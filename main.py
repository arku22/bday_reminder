import openpyxl as opex
import datetime as dt
from sms_config import send_message
from pathlib import Path


# read in source data worksheet
source_data = Path('.', 'sample_events.xlsx')  # set path & name of source file here
wb = opex.load_workbook(source_data)
sheet = wb.active
data_end_row = sheet.max_row
curr_year = dt.date.today().year
DATA_START_ROW = 2
HEADS_UP_DAYS = 1   # set here how many days ahead you want a reminder
HEADS_UP_DELTA = dt.timedelta(days=HEADS_UP_DAYS)

# parse sheet for any events that need a reminder
for row_num in range(DATA_START_ROW, data_end_row+1):

    event_date = sheet['A'+str(row_num)].value

    if dt.date.today() == (event_date.date()-HEADS_UP_DELTA):
        event_name = sheet['C'+str(row_num)].value
        event_type = sheet['B' + str(row_num)].value
        body = f"Today is {event_name}'s {event_type}!"

        send_message(body)
