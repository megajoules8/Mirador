import streamlit as st
import pandas as pd
import unicodedata

# Normalize function to remove accents and convert to lowercase
def normalize_string(input_str: str) -> str:
    return ''.join(
        char for char in unicodedata.normalize('NFD', input_str)
        if unicodedata.category(char) != 'Mn'
    ).lower()

# Load data
@st.cache_data
def load_data(filename: str) -> pd.DataFrame:
    df = pd.read_csv(filename)
    df['NormalizedWord'] = df['Word'].apply(normalize_string)
    return df

# Function to switch language
def get_text(key, language):
    language = language.lower()  # Convert to lowercase for matching dictionary keys
    texts = {
        "title": {"en": "Irish Words Search", "ga": "Cuardach ar Fhocail na Gaeilge"},
        "enter_substring": {"en": "Enter morpheme to search:", "ga": "Cuir moirféim isteach chun cuardach a dhéanamh:"},
        "search_type": {"en": "Search type:", "ga": "Cineál cuardaigh:"},
        "begins_with": {"en": "Begins with", "ga": "A thosaíonn le"},
        "ends_with": {"en": "Ends with", "ga": "A chríochnaíonn le"},
        "contains": {"en": "Contains", "ga": "Áit ar bith"},
        "search": {"en": "Search", "ga": "Cuardaigh"},
        "reset": {"en": "Reset", "ga": "Bánaigh"},
        "no_results": {"en": "No results found.", "ga": "Níor aimsíodh aon toradh."},
        "invalid_search": {"en": "Please enter a valid substring.", "ga": "Cuir cuardach bailí isteach."},
        "footer": {
            "en": """Type any part of a word you would like results for and then select if you would like results to "begin with", "contain", or "end with" those letters.<br>
            Note: partial matches with and without accents are included in results.<br><br> 
            <b>Creators</b><br>
            <u>Mykalin Jones</u>: Development<br>
            <u>Ellen Corbett</u>: Translation and Concept<br><br>
            <b>About Us</b><br>
            Mykalin Jones is a data scientist, curriculum writer, instructor, and passionate learner of the Irish language. <br>
            <a href="https://linktr.ee/ellencorbett">Ellen Corbett</a> is a PhD researcher, translator, and frequent user of Irish dictionaries.<br><br>
            """,
            "ga": """Cuir isteach an mhoirféim a bhfuil tú ag iarraidh a chuardach. Roghnaigh ar 
            mhaith leat torthaí “a thosaíonn le”, nó “a chríochnaíonn le” moirféim ar leith, 
            nó a bhfuil le feiceáil in “áit ar bith” san fhocal.<br>
            NB: cuirtear meaitseáil pháirteach le agus gan sínte fada san áireamh sna torthaí.<br><br>
            <b>Na Cruthaitheoirí</b><br>
            <u>Mykalin Jones</u> a d'fhobairt<br>
            <u>Ellen Corbett</u> a d'aistrigh agus a smaoinigh ar an choincheap<br><br>
            <b>Fúinn</b><br>
            Is eolaí sonraí, scríbhneoir curaclaim, agus teagascóir í Mykalin Jones. Tá a croí istigh sa Ghaeilge. <br>
            Is taighdeoir PhD agus aistritheoir í <a href="https://linktr.ee/ellencorbett">Ellen Corbett</a>. Is annamh lá nach mbíonn sí ag amharc ar fhoclóir Gaeilge.<br><br>
            """
        },
        "spinner": {"en": "Running...", "ga": "Ag rith..."},
        "match_type": {"en": "Match type:", "ga": "Cineál comhoiriúnachta:"},
        "partial_match": {"en": "Partial match", "ga": "Comhoiriúnacht pháirteach"},
        "exact_match": {"en": "Exact match", "ga": "Comhoiriúnacht iomlán"}
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
match_type = st.radio(get_text("match_type", language), [
    get_text("partial_match", language),
    get_text("exact_match", language)
])

# Load data
data = load_data("teanglann_words.csv")

# Search functionality
def search_words(data, substring, search_type, match_type):
    if match_type == get_text("exact_match", language):
        search_substring = substring
    else:
        search_substring = normalize_string(substring)
    
    normalized_substring = normalize_string(substring)
    
    if search_type == get_text("begins_with", language):
        result = data[data['NormalizedWord'].str.startswith(normalized_substring)]
    elif search_type == get_text("ends_with", language):
        result = data[data['NormalizedWord'].str.endswith(normalized_substring)]
    elif search_type == get_text("contains", language):
        result = data[data['NormalizedWord'].str.contains(normalized_substring)]
    else:
        result = pd.DataFrame(columns=['Word', 'Link'])

    return result.sort_values(by='Word')

# Convert DataFrame to HTML with clickable links
def df_to_clickable_html(df):
    df['Link'] = df.apply(lambda row: f'<a href="{row["Link"]}" target="_blank">{row["Link"]}</a>', axis=1)
    return df[['Word', 'Link']].to_html(escape=False, index=False)

# Columns for search and reset buttons
col1, col2, col3 = st.columns([3, 3, 1])
with col1:
    if st.button(get_text("search", language)):
        if not substring:
            st.error(get_text("invalid_search", language))
        else:
            result = search_words(data, substring, search_type, match_type)
            num_results = len(result)
            if result.empty:
                st.warning(get_text("no_results", language))
            else:
                st.write(f"Number of results: {num_results}")
                st.write(df_to_clickable_html(result), unsafe_allow_html=True)

with col3:
    if st.button(get_text("reset", language)):
        st.experimental_rerun()

# Footer
footer_text = get_text('footer', language).replace('\n', '<br>')
st.markdown(f"<footer style='text-align: left; padding: 10px 0;'>{footer_text}</footer>", unsafe_allow_html=True)
