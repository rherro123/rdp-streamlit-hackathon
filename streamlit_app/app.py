import traceback

import streamlit as st

def main() -> None:
    welcome = st.Page("pages/welcome.py", title="Welcome", icon=":material/home:", default=True)

    print("Hello World")
    pg = st.navigation(
        {
            "App": [welcome],
        }
    )

    pg.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        raise e
