import os
import smtplib
import ssl
from email.message import EmailMessage
import time
import sqlite3


import requests
import selectorlib

URL = 'https://programmer100.pythonanywhere.com/tours/'
USERNAME = 'peychev.vn@gmail.com'
PASSWORD = os.getenv('PASSWORD')

# Example queries

"INSERT INTO events VALUES ('Monkey', 'Monkey City', '2099.10.10')"
"SELECT * FROM events WHERE date='2099.10.10'"
"DELETE FROM events WHERE band='Tigers'"

# As we need to create the DB connection once we not need to set that in the method
connection = sqlite3.connect('data.db')

def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url)
    text = response.text
    return text


def extract(page_content):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(page_content)['tours']
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
    """Stored the extract info in file, so we can check if the info is already sent to prevent sending spam mails"""
    # with open('data.txt', 'a') as f:
    #     f.write(extracted + '\n')

    #SQL
    row = extracted.split(',')
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute('INSERT INTO events VALUES(?,?,?)', row)
    connection.commit()



def read(extracted):
    # With text file
    # with open('data.txt', 'r') as f:
    #     return f.read()

    # With SQL query
    row = extracted.split(',')
    row = [item.strip() for item in row]
    # Assign each variable to a part of the tuple list
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM events WHERE band=? AND city=? AND date=?', (band, city, date))
    rows = cursor.fetchall()
    print(rows)
    return rows

if __name__ == '__main__':
    # Run the script after some period of time
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)

        # content = read(extracted)
        if extracted != 'No upcoming tours':
            row = read(extracted)
            # if extracted not in content:

            # Check if the row values exist, if not EMPTY row
            if not row:
                store(extracted)
                send_email(USERNAME, extracted, extracted)

        # Set the time of the script run pause
        time.sleep(2)

# another option is Python anywhere from day 28, but it is subscription service
