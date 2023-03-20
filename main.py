from sms_reminder import SMSReminder
from pathlib import Path


excel_file_path = Path('.', 'events.xlsx')
s_reminder = SMSReminder(excel_file_path=excel_file_path,
                         heads_up_days=0)

s_reminder.send_event_reminder()

