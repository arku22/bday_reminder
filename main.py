import datetime as dt
from sms_config import send_message
from pathlib import Path
import pandas as pd

def send_sms(row: pd.Series) -> None:
    """
    Builds sms message body and sends out sms
    :param row: pd.Series
    :return: None
    """
    sms_body = f"Today is {row['event_name']}'s {row['event_type']}!"
    send_message(sms_body)

    return


# read in source data worksheet
source_data = Path('.', 'sample_events.xlsx')  # set path & name of source file here
df = pd.read_excel(source_data,
                   sheet_name=0,
                   parse_dates=['event_month_day'])
df['event_month_day'] = df['event_month_day'].dt.date
HEADS_UP_DAYS = 0   # set here how many days ahead you want a reminder
heads_up_days_delta = dt.timedelta(days=HEADS_UP_DAYS)

# parse sheet for any events that need a reminder
df_alert_events = df.loc[(df['event_month_day']-heads_up_days_delta) == dt.date.today()]

# send out sms alerts for events that are due
df_alert_events.apply(send_sms, axis=1)

