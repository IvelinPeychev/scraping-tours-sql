import requests
import selectorlib

URL = 'https://programmer100.pythonanywhere.com/tours/'


def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url)
    text = response.text
    return text


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)['tours']
    return value


def send_email():
    print('Email was sent!')


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
            send_email()
