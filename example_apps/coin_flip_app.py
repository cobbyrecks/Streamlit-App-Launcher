import streamlit as st
import random


def main():
    st.title("Simple Coin Flip App")

    # Button to flip the coin
    if st.button("Flip Coin"):
        result = flip_coin()
        st.write(f"The coin landed on: {result}")


def flip_coin():
    result = random.choice(["Heads", "Tails"])
    return result


if __name__ == "__main__":
    main()
