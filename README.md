# BIRTHDAY REMINDER SCRIPT

I have been embarrased far too many times by my friends wishing me a happy birthday while I keep forgetting their birthday year after year. This is my attempt at making up for it.

This is a simple Python script that sends you a reminder via SMS using the Twilio SMS gateway.

---

## Technologies

* Python 3.8.11
* Google Sheets
* twilio 6.63.2
* openpyxl 3.0.7
* git 2.36.1
* Pycharm 2022
For a more detailed list of python libraries used refer to the `requirements.txt` file in the working directory.

---

## Table of Contents

1. [Setup](#setup)
2. [Create a Twilio account](#creating-a-twilio-account)
3. [Modifying Project Files](#modifying-the-project-files)
4. [Installing Python Dependencies](#installing-python-dependencies)
5. [Running the Program](#running-the-program)
6. [Scheduling the program to run automatically](#scheduling-the-program-to-run-automatically)

---
## Setup

To use this repo for you own purposes, open the terminal (Mac/Linux) or the command prompt (Windows) & run the following:

```
$ cd ~/Desktop
$ git clone https://github.com/arku22/bday_reminder.git
```

### Creating a Twilio account

1. Navigate to [Twilio - Register](https://www.twilio.com/try-twilio)
2. Grab the following details from your Twilio dashboard once registered:
	- Account SID
	- Auth Token
	- Twilio phone number
3. You will also have to verify the phone number with Twilio, where you want to receive the SMS (Needed for the trial account for Twilio).


### Modifying the project files

1. Modify `.sample_env`:
	- Open `sample_env` and replace the `< >` with the values from your twilio account
	- Rename the file to `.env`
2. Modify `sample_events.xlsx`:
	- Delete existing rows & write in the dates that you want to get a reminder for
	- **NOTE**: Do NOT alter the header row. This will cause the code to fail to run. Also, delete any blank rows in the excel sheet.
3. Modify `main.py`:
	- Set the number of days you want to receive the reminder ahead of the actual event using the `heads_up_days` variable in the python file. Default is set to one day ahead of the actual event/birthday.

### Installing python dependencies

Run the following:

`$ cd ~/Desktop/bday_reminder`

If using 'Anaconda' for virtual environments:

`$ conda env create --file environment.yaml`

otherwise, if using 'pip' then:

`$ pip install -r requirements.txt`

### Running the program:

`$ python main.py`

---

## Scheduling the program to run automatically

This program would of course not be useful if you had to run it manually on your computer every single time. The way to go about it is to have it scheduled to run on a server. Possible ways of achieving this are:

1. [Python Anywhere](https://www.pythonanywhere.com)
2. [Amazon EC2](https://aws.amazon.com/aws/ec2), 'cron' job
3. [Raspberry Pi](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)

These are some of many possible ways to allow the script to be run automatically once a day and check whether there are any reminders that need to be sent via SMS. I used a paid account on 'Python Anywhere', although it might be cheaper to use Amazon EC2.
