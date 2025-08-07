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
    st.sidebar.title("Nav")
    st.sidebar.markdown(
        """
        <div style='margin-top:50px; margin-bottom:20px;'>
            <button style='width:100%; height:40px;'>Custom Button 1</button>
        </div>
        <div style='margin-top:100px;'>
            <button style='width:100%; height:40px;'>Custom Button 2</button>
        </div>
        <div style='margin-top:100px;'>
            <button style='width:100%; height:40px;'>Custom Button 3</button>
        </div>
        <div style='margin-top:100px;'>
            <button style='width:100%; height:40px;'>Custom Button 4</button>
        </div>
        """,
        unsafe_allow_html=True
    )
    

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div style=' position: fixed; left: 0; bottom: 0; height:300px; border:2px solid #CCC; padding:10px; border-radius:8px;'>Container 1</div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div style='position: fixed; left: 50%; bottom: 0; height:300px; border:2px solid #CCC; padding:10px; border-radius:8px;'>Container 2</div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div style='position: fixed; right: 0; bottom: 0;height:300px; border:2px solid #CCC; padding:10px; border-radius:8px;'>Container 3</div>
            """,
            unsafe_allow_html=True
        )


main()
