import streamlit as st


def main():
    st.title("Simple Calculator App")

    num1 = st.number_input("Enter the first number:")
    num2 = st.number_input("Enter the second number:")

    operation = st.selectbox("Select operation", ["+", "-", "*", "/"])

    result = 0

    if operation == "+":
        result = num1 + num2
    elif operation == "-":
        result = num1 - num2
    elif operation == "*":
        result = num1 * num2
    elif operation == "/":
        if num2 != 0:
            result = num1 / num2
        else:
            st.error("Cannot divide by zero")

    st.write("Result:", result)


if __name__ == "__main__":
    main()
