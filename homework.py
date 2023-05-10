import requests
import selectorlib
import time
import streamlit as st
import plotly.express as px
import sqlite3

URL = 'https://programmer100.pythonanywhere.com/'
connection = sqlite3.connect('data.db')

def send_request(url):
    response = requests.get(url)
    text = response.text
    return text

def extract_info(page_content):
    extractor = selectorlib.Extractor.from_yaml_file('homework.yaml')
    target_info = extractor.extract(page_content)['temperature']
    return target_info


def store_info(info):
    # In file
    # with open('homework.txt', 'a') as f:
    #     f.write(info + '\n')

    # In DB
    cursor = connection.cursor()
    cursor.execute('INSERT INTO temperature VALUES(?,?)',info)
    connection.commit()

# def read_file(filename):
    # From file
    # with open(filename, 'r') as f:
    #     return f.readlines()


def read_db():
    # From DB
    cursor = connection.cursor()
    cursor.execute('Select * FROM temperature')

    rows = cursor.fetchall()
    print(rows)
    return rows


if __name__ == '__main__':
    # Get the page source response
    response = send_request(URL)

    # Extract the target info
    temperature = extract_info(response)
    print(temperature)

    # Get the date and time
    date_and_time = time.strftime('%y-%m-%d-%H-%M-%S')
    print(date_and_time)

# TEXT FILE APPROACH
#     # Store the date and temperature in a file
#     info = f"{date_and_time}, {temperature}"
#     store_info(info)
#
#     # Load the file as it will be needed for extract the values for the graph
#     info_in_file = read_file('homework.txt')[1:]
#
#     # Extracting data needed for the graph
#     dates = [row.split(', ')[0] for row in info_in_file]
#     temperatures = [row.split(', ')[1] for row in info_in_file]
#
#     # Start the web app
#     st.title('')
#
#     # Config the figure
#     figure = px.line(x=dates, y=temperatures, labels={'x': 'Date', 'y': 'Temperature (C)'})
#
#     # Display the figure
#     st.plotly_chart(figure)

# SQL DB APPROACH
    info = (temperature, date_and_time)
    store_info(info)
    graph_data = read_db()
    temp = [data[0] for data in graph_data]
    date = [data[1] for data in graph_data]

    # Start the web app
    st.title('')

    # Config the figure
    figure = px.line(x=date, y=temp, labels={'x': 'Date', 'y': 'Temperature (C)'})

    # Display the figure
    st.plotly_chart(figure)
