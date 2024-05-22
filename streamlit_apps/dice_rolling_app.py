import streamlit as st
import random


def main():
    st.title("Simple Dice Rolling App")

    # Dropdown to select the number of dice
    num_dice = st.selectbox("Select number of dice:", [1, 2, 3, 4, 5])

    # Button to roll the dice
    if st.button("Roll Dice"):
        results = roll_dice(num_dice)
        st.write("The dice rolled:")
        for i, result in enumerate(results):
            st.write(f"Dice {i+1}: {result}")


def roll_dice(num_dice):
    results = [random.randint(1, 6) for _ in range(num_dice)]
    return results


if __name__ == "__main__":
    main()
