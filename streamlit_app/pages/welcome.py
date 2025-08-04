import sqlite3
from datetime import datetime

import streamlit as st


def connect_to_db():
    connection = sqlite3.connect('times.db')
    c = connection.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS times (id INTEGER PRIMARY KEY AUTOINCREMENT, time TEXT)')
    connection.commit()
    return connection, c


def add_time(connection, c):
    time = datetime.now().strftime('%H:%M:%S')
    c.execute('INSERT INTO times (time) VALUES (?)', (time,))
    connection.commit()


def delete_latest_time(connection, c):
    c.execute('DELETE FROM times WHERE id = (SELECT MAX(id) FROM times)')
    connection.commit()


def display_all_times(c):
    c.execute('SELECT time FROM times')
    times = c.fetchall()
    time_str = '\n\n'.join([t[0] for t in times])
    st.info(time_str)


def main():
    connection, cursor = connect_to_db()

    st.markdown('''### Welcome to the RDP Hackathon!
    This app uses Streamlit, Python and SQLite.''')

    if st.button('Add Current Time'):
        add_time(connection, cursor)

    if st.button('Remove Last Time'):
        delete_latest_time(connection, cursor)

    display_all_times(cursor)

    connection.close()


main()
