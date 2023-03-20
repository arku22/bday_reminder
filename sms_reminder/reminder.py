from twilio.rest import Client
from dotenv import load_dotenv
import os
from pathlib import Path
import pandas as pd
import datetime as dt


# load required environment variables
load_dotenv()

class SMSReminder:
    """
    A class that sends SMS reminders by reading through an Excel sheet and finding events that need a reminder sent out
    """

    def __init__(self,
                 excel_file_path=Path('.', 'sample_events.xlsx'),
                 heads_up_days=0):

        self.acc_sid = os.getenv("twi_account_SID")     # get this from your twilio account
        self.auth_token = os.getenv("twi_auth_token")   # get this from your twilio account
        self.twilio_sender = os.getenv("twi_sender_num")  # twilio phone number to send SMS
        self.receiver = os.getenv("receiver_num")   # twilio verified phone number to  receive SMS
        self.excel_file_path = excel_file_path
        self.heads_up_days = heads_up_days  # Number of days ahead of the event the SMS should go out

    def get_reminder_events(self, excel_file_path) -> pd.DataFrame:
        """
        This will parse the Excel worksheet for the events for which an SMS reminder is due at runtime
        :return: pd.DataFrame of events filtered from Excel source
        """
        source_data = excel_file_path
        df = pd.read_excel(source_data,
                           sheet_name=0,
                           parse_dates=['event_month_day'])
        df['event_month_day'] = df['event_month_day'].dt.date
        heads_up_days_delta = dt.timedelta(days=self.heads_up_days)

        # parse sheet for any events that need a reminder
        df_alert_events = df.loc[(df['event_month_day'] - heads_up_days_delta) == dt.date.today()]

        return df_alert_events

    def send_sms(self, row: pd.Series) -> None:
        """
            Builds sms message body and send out sms using twilio
            :param row: pd.Series
            :return: None
            """
        sms_body = f"Today is {row['event_name']}'s {row['event_type']}!"

        tcli = Client(self.acc_sid, self.auth_token)
        message = tcli.messages.create(body=sms_body,
                                       from_=self.twilio_sender,
                                       to=self.receiver)
        return None

    def send_event_reminder(self) -> None:
        """
        Send out SMS reminder for due events
        :return: None
        """
        df = self.get_reminder_events(self.excel_file_path)
        df.apply(self.send_sms, axis=1)

        return None


if __name__ == "__main__":
    excel_path = Path('.', 'sample_events.xlsx')
    s_reminder = SMSReminder(excel_file_path=excel_path,
                             heads_up_days=0)
    s_reminder.send_event_reminder()
