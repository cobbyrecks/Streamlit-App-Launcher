import streamlit as st
import re


def count_words(text):
    # Count number of words
    word_count = len(text.split())

    # Count number of characters (excluding spaces)
    char_count = len(text.replace(" ", ""))

    # Count number of sentences
    sentence_count = len(re.findall(r'[.?!]', text))

    return word_count, char_count, sentence_count


def main():
    st.title("Simple Word Counter App")

    # Text input for user input
    user_input = st.text_area("Enter text:")

    if st.button("Count"):
        if user_input:
            word_count, char_count, sentence_count = count_words(user_input)
            st.write(f"Number of words: {word_count}")
            st.write(f"Number of characters: {char_count}")
            st.write(f"Number of sentences: {sentence_count}")
        else:
            st.warning("Please enter some text.")


if __name__ == "__main__":
    main()
