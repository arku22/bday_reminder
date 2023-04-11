from sms_reminder import SMSReminder
from pathlib import Path


base_dir = Path(__file__).parent
excel_file_path = Path(base_dir, 'events.xlsx')
s_reminder = SMSReminder(heads_up_days=0)

s_reminder.send_event_reminder()

