import pandas as pd
import streamlit as st
import unicodedata

# Normalize function to remove accents and convert to lowercase
def normalize_string(input_str: str) -> str:
    return ''.join(
        char for char in unicodedata.normalize('NFD', input_str)
        if unicodedata.category(char) != 'Mn'
    ).lower()

@st.cache_data
def load_data(filename: str) -> pd.DataFrame:
    df = pd.read_csv(filename)
    df['NormalizedWord'] = df['Word'].apply(normalize_string)
    return df

# Function to filter words based on search criteria
def filter_words(words: pd.DataFrame, substring: str, search_type: str) -> pd.DataFrame:
    normalized_substring = normalize_string(substring)
    if search_type == 'begins':
        return words[words['NormalizedWord'].str.startswith(normalized_substring)]
    elif search_type == 'ends':
        return words[words['NormalizedWord'].str.endswith(normalized_substring)]
    elif search_type == 'contains':
        return words[words['NormalizedWord'].str.contains(normalized_substring)]
    else:
        raise ValueError("Invalid search_type. Choose from 'begins', 'ends', or 'contains'.")

# Streamlit UI
st.title("Irish Words Search")

# Load data from CSV
words_df = load_data('teanglann_words.csv')

substring = st.text_input("Enter substring to search for:")
search_type = st.selectbox("Search type:", ['begins', 'ends', 'contains'])

if st.button("Search"):
    filtered_words = filter_words(words_df, substring, search_type)
    filtered_words = filtered_words[['Word', 'Link']]
    filtered_words['Link'] = filtered_words['Link'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>')
    st.write(filtered_words.to_html(escape=False, index=False), unsafe_allow_html=True)
