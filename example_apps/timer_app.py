import streamlit as st
import time


def main():
    st.title("Simple Timer App")

    duration = st.number_input("Enter duration in seconds:", min_value=1)

    if st.button("Start Timer"):
        start_timer(duration)


def start_timer(duration):
    with st.spinner("Timer is running..."):
        time.sleep(duration)
        st.success("Timer is up!")


if __name__ == "__main__":
    main()
