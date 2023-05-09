import os
import smtplib
import ssl
from email.message import EmailMessage

import requests
import selectorlib

URL = 'https://programmer100.pythonanywhere.com/tours/'
USERNAME = 'peychev.vn@gmail.com'
PASSWORD = os.getenv('PASSWORD')


def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url)
    text = response.text
    return text


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)['tours']
    return value


def send_email(from_email, subject, message):
    """
        Sends an email via the above SMTP server. All comms go through SSL.
        :param from_email: address of the sender.
        :param subject: subject for the message.
        :param message: the main text of the message.
        """
    host = 'smtp.gmail.com'
    port = 465

    receiver = 'peychev.vn@gmail.com'
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(USERNAME, PASSWORD)


        # Construct the email
        msg = EmailMessage()
        msg['From'] = from_email
        msg['To'] = receiver
        msg['Subject'] = subject
        msg.set_content(f'You have new upcoming event - {message}')

        server.send_message(msg)
        server.set_debuglevel(1)


def store(extracted):
    """Stored the extract info in file so we can check if the info is already sent to prevent sending spam mails"""
    with open('data.txt', 'a') as f:
        f.write(extracted + '\n')


def read(extracted):
    with open('data.txt', 'r') as f:
        return f.read()

if __name__ == '__main__':
    scraped = scrape(URL)
    extracted = extract(scraped)
    print(extracted)

    content = read(extracted)
    if extracted != 'No upcoming tours':
        if extracted not in content:
            store(extracted)
            send_email(USERNAME, extracted, extracted)
