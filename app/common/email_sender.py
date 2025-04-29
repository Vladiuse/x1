import os
from dataclasses import dataclass

from common.exceptions import EmailNotSend
from common.request_sender import RequestSender
from dotenv import load_dotenv
from requests.exceptions import RequestException

load_dotenv()
EMAIL_JS_API_URL = 'https://api.emailjs.com/api/v1.0/email/send'
headers = {
    'Content-Type': 'application/json',
}


@dataclass
class EmailData:
    reset_password_code: int
    email: str
    reset_url: str


class EmailSender:
    def __init__(self, request_sender: RequestSender):
        self.request_sender = request_sender

    def send_email(self, email_data: EmailData) -> None:
        data = {
            'service_id': os.environ.get('SERVICE_ID'),
            'template_id': os.environ.get('TEMPLATE_ID'),
            'user_id': os.environ.get('PUBLIC_KEY'),
            'template_params': {
                'reset_password_code': email_data.reset_password_code,
                'email': email_data.email,
                'reset_url': email_data.reset_url,
            },
        }
        try:
            self.request_sender.request(
                url=EMAIL_JS_API_URL,
                method='POST',
                json=data,
                headers=headers,
                attempts=2,
            )
        except RequestException as error:
            raise EmailNotSend(f'Cant send email to {email_data.email}: {error}')
