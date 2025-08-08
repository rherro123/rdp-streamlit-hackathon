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
    # st.markdown(
    #     """
    #     <div style='
    #         position: fixed;
    #         top: 48px;
    #         left: 0;
    #         width: 100%;
    #         height: 60px;
    #         background-color: #f0f2f6;
    #         border-bottom: 2px solid #CCC;
    #         display: flex;
    #         align-items: center;
    #         padding-left: 20px;
    #         font-size: 24px;
    #         font-weight: bold;
    #         z-index: 1000;
    #     '>
    #         My Top Bar
    #     </div>
    #     <div style='height:70px;'></div> <!-- Spacer to prevent overlap -->
    #     """,
    #     unsafe_allow_html=True
    # )
    
    st.sidebar.title("Home")
    st.sidebar.markdown(
        """
        <div style='margin-top:50px; margin-bottom:20px;'>
            <button style='width:100%; height:40px;'>SKU's</button>
        </div>
        <div style='margin-top:100px;'>
            <button style='width:100%; height:40px;'>Lanes</button>
        </div>
        <div style='margin-top:100px;'>
            <button style='width:100%; height:40px;'>Orders</button>
        </div>
        <div style='margin-top:100px; position: fixed; bottom: 20px; width: 8.3%'>
            <button style='width:100%; height:40px;'>Settings</button>
        </div>
        """,
        unsafe_allow_html=True
    )

    filter = st.selectbox(
        "Filter",
        ["All", "Last 24 hours", "Last 7 days", "Last 30 days"]
    )

    show_col1 = filter != "All"

    col1, col2, col3 = st.columns(3)

    if show_col1:
        with col1:
            st.markdown(
                """
                <div style=' position: fixed; left: 10.15%; bottom: 0; height:600px; width:29.95%; border:2px solid #CCC; padding:10px; border-radius:8px;'>Container 1</div>
                """,
                unsafe_allow_html=True
            )

    with col2:
        st.markdown(
            """
            <div style='position: fixed; left: 40%; bottom: 0; height:600px; width:29.95%; border:2px solid #CCC; padding:10px; border-radius:8px;'>Container 2</div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div style='position: fixed; right: 0; bottom: 0; height:1050px; width:29.95%; border:2px solid #CCC; padding:10px; border-radius:8px;'>Container 3</div>
            """,
            unsafe_allow_html=True
        )


main()
