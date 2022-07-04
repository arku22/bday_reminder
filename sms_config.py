from twilio.rest import Client
from dotenv import load_dotenv
import os


# load required environment variables
load_dotenv()
acc_sid = os.getenv("twi_account_SID")
auth_token = os.getenv("twi_auth_token")
twilio_sender = os.getenv("twi_sender_num")    # twilio phone number to send SMS
receiver = os.getenv("receiver_num")      # twilio verified phone number to  receive SMS (needed with twilio trial acc.)


def send_message(body):
    """
    This function simply creates an SMS message and sends it via Twilio
    :param body: str- contents of the SMS
    :return: None
    """
    tcli = Client(acc_sid, auth_token)
    message = tcli.messages.create(body=body, from_=twilio_sender, to=receiver)
    return None

