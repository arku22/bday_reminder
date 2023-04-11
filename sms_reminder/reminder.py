from twilio.rest import Client
from dotenv import load_dotenv
import os
import pandas as pd
import datetime as dt
import psycopg2
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


# load required environment variables
load_dotenv()


class SMSReminder:
    """
    A class that sends SMS reminders by querying a postgres database and finding events that need a reminder sent out
    """

    def __init__(self,
                 heads_up_days=0):

        self.acc_sid = os.getenv("twi_account_SID")     # get this from your twilio account
        self.auth_token = os.getenv("twi_auth_token")   # get this from your twilio account
        self.twilio_sender = os.getenv("twi_sender_num")  # twilio phone number to send SMS
        self.receiver = os.getenv("receiver_num")   # twilio verified phone number to receive SMS
        self.heads_up_days = heads_up_days  # Number of days ahead of the event the SMS should go out

    def get_reminder_events(self) -> pd.DataFrame:
        """
        This will read records from a postgres database events for which an SMS reminder is due at runtime
        :return: pd.DataFrame of events filtered with due reminders
        """
        conn = psycopg2.connect(database=os.environ.get("database_name"),
                                user=os.environ.get("database_user"),
                                password=os.environ.get("database_user_password"),
                                host=os.environ.get("database_host"),
                                port=os.environ.get("database_port"))

        # read sql query to query database
        with open(Path(Path(__file__).parents[1], "assets/sql/get_event_reminders.sql"), 'r') as f:
            sql_query = f.read()
        df = pd.read_sql_query(sql_query, conn)

        df["event_date"] = pd.to_datetime(df["event_date"], format="%m-%d").dt.date
        df["event_date"] = df["event_date"].apply(lambda x: x.replace(year=2023))

        heads_up_days_delta = dt.timedelta(days=self.heads_up_days)

        # parse data for any events that need a reminder
        df_alert_events = df.loc[(df['event_date'] - heads_up_days_delta) == dt.date.today()]

        return df_alert_events

    def send_sms(self, row: pd.Series) -> None:
        """
            Builds sms message body and send out sms using twilio
            :param row: pd.Series
            :return: None
            """

        # use jinja2 template to build sms body
        environment = Environment(loader=FileSystemLoader("templates/"))
        sms_template = environment.get_template("sms_template.txt")
        context = {"event_date": row["event_date"],
                   "event_day_name": row["event_date"].strftime("%A"),
                   "event_type": row["event_type"],
                   "first_name": row["first_name"],
                   "last_name": row["last_name"],
                   "addnt_identifier": row["addnt_identifier"],
                   "event_country": row["country_code"]}
        sms_body = sms_template.render(context)

        tcli = Client(self.acc_sid, self.auth_token)    # init twilio client
        # send sms
        message = tcli.messages.create(body=sms_body,
                                       from_=self.twilio_sender,
                                       to=self.receiver)
        return None

    def send_event_reminder(self) -> None:
        """
        Send out SMS reminder for due events
        :return: None
        """
        df = self.get_reminder_events()
        if not df.empty:    # only send out sms if due events were found
            df.apply(self.send_sms, axis=1)

        return None
