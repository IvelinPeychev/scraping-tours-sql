import requests
import selectorlib
import time
import streamlit as st
import plotly.express as px

URL = 'https://programmer100.pythonanywhere.com/'


def send_request(url):
    response = requests.get(url)
    text = response.text
    return text

def extract_info(page_content):
    extractor = selectorlib.Extractor.from_yaml_file('homework.yaml')
    target_info = extractor.extract(page_content)['temperature']
    return target_info


def store_info(info):
    with open('homework.txt', 'a') as f:
        f.write(info + '\n')


def read_file(filename):
    with open(filename, 'r') as f:
        return f.readlines()


if __name__ == '__main__':
    # Get the page source response
    response = send_request(URL)

    # Extract the target info
    temperature = extract_info(response)
    print(temperature)

    # Get the date and time
    date_and_time = time.strftime('%y-%m-%d-%H-%M-%S')
    print(date_and_time)

    # Store the date and temperature in a file
    info = f"{date_and_time}, {temperature}"
    store_info(info)

    # Load the file as it will be needed for extract the values for the graph
    info_in_file = read_file('homework.txt')[1:]

    # Extracting data needed for the graph
    dates = [row.split(', ')[0] for row in info_in_file]
    temperatures = [row.split(', ')[1] for row in info_in_file]

    # Start the web app
    st.title('')

    # Config the figure
    figure = px.line(x=dates, y=temperatures, labels={'x': 'Date', 'y': 'Temperature (C)'})

    # Display the figure
    st.plotly_chart(figure)
