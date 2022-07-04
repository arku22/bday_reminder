import openpyxl as opex
import datetime as dt
from sms_config import send_message
from pathlib import Path


# read in source data worksheet
source_data = Path('.', 'sample_events.xlsx')  # set path & name of source file here
wb = opex.load_workbook(source_data)
sheet = wb.active
end = sheet.max_row
curr_year = dt.date.today().year
data_start_row = 2
heads_up_days = 1   # set here how many days ahead you want a reminder
heads_up_delta = dt.timedelta(days=heads_up_days)

# parse sheet for any events that need a reminder
for row_num in range(data_start_row, sheet.max_row+1):
    event_day = int(sheet['A'+str(row_num)].value)
    event_month = int(sheet['B'+str(row_num)].value)
    event_date = dt.date(year=curr_year, month=event_month, day=event_day)
    if dt.date.today() == (event_date-heads_up_delta):
        event_name = sheet['D'+str(row_num)].value
        event_type = sheet['C' + str(row_num)].value
        body = f"Today is {event_name}'s {event_type}!"

        send_message(body)
