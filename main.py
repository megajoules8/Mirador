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
        "title": {"en": "Míreadóir: Search Irish-language Morphemes", "ga": "Míreadóir: Cuardaigh Moirféimí na Gaeilge"},
        "enter_substring": {"en": "Enter morpheme to search:", "ga": "Cuir moirféim isteach chun cuardach a dhéanamh:"},
        "search_type": {"en": "Search type:", "ga": "Cineál cuardaigh:"},
        "begins_with": {"en": "Begins with", "ga": "A thosaíonn le"},
        "ends_with": {"en": "Ends with", "ga": "A chríochnaíonn le"},
        "contains": {"en": "Contains", "ga": "ÁIT ar bith"},
        "search": {"en": "Search", "ga": "Cuardaigh"},
        "no_results": {"en": "No results found.", "ga": "Place holder."},
        "invalid_search": {"en": "Please enter a valid substring.", "ga": "Place holder."},
        "footer": {
            "en": """<b>App Information</b><br>
            Type any part of a word you would like results for and then select if
            you would like results to "begin with", "contain", or "end with" those letters.<br>
            Note: partial matches with and without síntí fada are included in results.<br><br>
            <b>Creators</b><br>
            <u>Development</u>: Mykalin Jones<br>
            <u>a literal Queen</u>: Ellen Corbett<br><br>
            <b>About Us</b><br>
            <u>Mykalin Jones</u>: Is eolaí sonraí, scríbhneoir curaclaim, agus teagascóir í Mykalin Jones/Mícheáilín Nic Sheoin. Tá a croí istigh sa Ghaeilge.<br><br>
            <u>Ellen Corbett</u>: Ellen Corbett (she/her) is a PhD researcher, translator, and frequent user of Irish dictionaries.<br><br>
            <b>Míreadóir</b><br>
            Míreadóir [Mir-a-door] enables users to search for specific Irish-language morphemes including suffixes, prefixes, and other affixes.
            Morphemes can denote declension, gender, case, and number. However, the ability to search for specific morphemes is not currently available through other online resources, despite its usefulness.
            Taking inspiration from the Spanish mirador, we hope that this resource will provide a new vantage point from which to view Irish mír. We hope that Míreadóir will be useful to Irish-language learners and teachers, translators, writers, language professionals, or anyone interested in the language.
            """,            
            "ga": """<b>App Information</b><br>
            This is an app to search for Irish words by any substring.<br>
            To use, type any part of a word you would like results for and then select if
            you would like results to "begin with", "contain", or "end with" those letters.<br>
            Note: partial matches with and without síntí fada are included in results.<br><br>
            <b>Creators</b><br>
            <u>Development</u>: Mykalin Jones<br>
            <u>a literal Queen</u>: Ellen Corbett<br><br>
            <b>About Us</b><br>
            <u>Mykalin Jones</u>: Place Holder <br>
            <u>Ellen Corbett</u>: Place Holder<br><br>
            <b>Míreadóir</b><br>
            <u>Development</u>: Mykalin Jones
            """,
        },
        "spinner": {"en": "Running...", "ga": "Ag rith..."}
    }
    return texts[key][language]

# Streamlit UI
logo = "mireadoir.png"  # Update with the path to your logo

# Sidebar with logo and language selection
with st.sidebar:
    st.image(logo, width=250)
    language = st.selectbox("Roghnaigh teanga / Select Language:", ['GA', 'EN'], index=0)

# App title
st.title(get_text("title", language))

# Input fields
substring = st.text_input(get_text("enter_substring", language))
search_type = st.selectbox(get_text("search_type", language), [
    get_text("begins_with", language),
    get_text("ends_with", language),
    get_text("contains", language)
])

# Load data
data = load_data("teanglann_words.csv")

# Search functionality
def search_words(data, substring, search_type):
    normalized_substring = normalize_string(substring)  # Normalize the search input
    if search_type == get_text("begins_with", language):
        return data[data['NormalizedWord'].str.startswith(normalized_substring)]
    elif search_type == get_text("ends_with", language):
        return data[data['NormalizedWord'].str.endswith(normalized_substring)]
    elif search_type == get_text("contains", language):
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
