import streamlit as st
import pandas as pd
import unicodedata

# Normalize function to remove accents and convert to lowercase
def normalize_string(input_str: str) -> str:
    return ''.join(
        char for char in unicodedata.normalize('NFD', input_str)
        if unicodedata.category(char) != 'Mn'
    ).lower()

# Load data (assuming the CSV file is available)
@st.cache_data
def load_data(filename: str) -> pd.DataFrame:
    df = pd.read_csv(filename)
    df['NormalizedWord'] = df['Word'].apply(normalize_string)
    return df

# Function to switch language
def get_text(key, language):
    texts = {
        "title": {"en": "Irish Word Search", "ga": "Place holder"},
        "enter_substring": {"en": "Enter substring to search for:", "ga": "Place holder:"},
        "search_type": {"en": "Search type:", "ga": "Place holder:"},
        "search": {"en": "Search", "ga": "Cuardach"},
        "no_results": {"en": "No results found.", "ga": "Place holder."},
        "invalid_search": {"en": "Please enter a valid substring.", "ga": "Place holder."},
        "footer": {
            "en": """This is an app to search for Irish words by any substring. 
To use, type any part of a word you would like results for and then select if
you would like results to "begin with", "contain", or "end with" those letters.
Note: partial matches with and without síntí fada are included in results.
Development: Mykalin Jones
Language Expertise: Ellen Corbett.""",
            "ga": "Place holder."
        },
        "spinner": {"en": "Running...", "ga": "Ag rith..."}
    }
    return texts[key][language]

# Streamlit UI
logo = "mireadoir.png"  # Update with the path to your logo

# Sidebar with logo and language selection
with st.sidebar:
    st.image(logo, width=250)
    language = st.selectbox("Place Holder / Select Language:", ['ga', 'en'], index=0)

# App title
st.title(get_text("title", language))

# Input fields
substring = st.text_input(get_text("enter_substring", language))
search_type = st.selectbox(get_text("search_type", language), ['begins', 'ends', 'contains'])

# Load data
data = load_data("teanglann_words.csv")

# Search functionality
def search_words(data, substring, search_type):
    normalized_substring = normalize_string(substring)  # Normalize the search input
    if search_type == 'begins':
        return data[data['NormalizedWord'].str.startswith(normalized_substring)]
    elif search_type == 'ends':
        return data[data['NormalizedWord'].str.endswith(normalized_substring)]
    elif search_type == 'contains':
        return data[data['NormalizedWord'].str.contains(normalized_substring)]
    return pd.DataFrame(columns=['Word', 'Link'])

# Convert DataFrame to HTML with clickable links
def df_to_clickable_html(df):
    df['Link'] = df.apply(lambda row: f'<a href="{row["Link"]}" target="_blank">{row["Link"]}</a>', axis=1)
    return df[['Word', 'Link']].to_html(escape=False, index=False)

# Perform search
if st.button(get_text("search", language)):
    if not substring:
        st.error(get_text("invalid_search", language))
    else:
        result = search_words(data, substring, search_type)
        if result.empty:
            st.warning(get_text("no_results", language))
        else:
            st.write(df_to_clickable_html(result), unsafe_allow_html=True)

# Footer
footer_text = get_text('footer', language).replace('\n', '<br>')
st.markdown(f"<footer style='text-align: left; padding: 10px 0;'>{footer_text}</footer>", unsafe_allow_html=True)
