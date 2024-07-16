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
        "title": {"en": "Míreadóir: Search Irish-language Morphemes", "ga": "Míreadóir: Cuardaigh Moirféimí na Gaeilge"},
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
            Note: partial matches with and without síntí fada are included in results.<br><br> 
            <b>Creators</b><br>
            <u>Mykalin Jones</u>: Development<br>
            <u>Ellen Corbett</u>: Translation and Concept<br><br>
            <b>Míreadóir</b><br>
            <i>Míreadóir</i> [Mir-a-door] enables users to search for specific Irish-language morphemes including suffixes, prefixes, and other affixes.<br>
            Morphemes can denote declension, gender, case, and number. However, the ability to search for specific morphemes is not currently available through other online resources, despite its usefulness.<br>
            Taking inspiration from the Spanish <i>mirador</i>, we hope that this resource will provide a new vantage point from which to view Irish <i>mír</i>. We hope that Míreadóir will be useful to Irish-language learners and teachers, translators, writers, language professionals, or anyone interested in the language.<br><br>
            <b>About Us</b><br>
            Mykalin Jones/Mícheáilín Nic Sheoin (she/her) is a data scientist, curriculum writer, instructor, and passionate learner of the Irish language. <br>
            <a href="https://linktr.ee/ellencorbett">Ellen Corbett</a> (she/her) is a PhD researcher, translator, and frequent user of Irish dictionaries.<br><br>
            """,
            "ga": """Cuir isteach an mhoirféim a bhfuil tú ag iarraidh a chuardach. Roghnaigh ar 
            mhaith leat torthaí “a thosaíonn le”, nó “a chríochnaíonn le” moirféim ar leith, 
            nó a bhfuil le feiceáil in “áit ar bith” san fhocal.<br>
            NB: cuirtear meaitseáil pháirteach le agus gan sínte fada san áireamh sna torthaí.<br><br>
            <b>Na Cruthaitheoirí</b><br>
            <u>Mykalin Jones</u> a d'fhobairt<br>
            <u>Ellen Corbett</u> a d'aistrigh agus a smaoinigh ar an choincheap<br><br>
            <b>Míreadóir</b><br>
            Ligeann Míreadóir d’úsáideoirí moirféimí na Gaeilge a chuardach, iarmhíreanna, réimíreanna, agus táthmhíreanna eile san áireamh.<br>
            Is féidir le moirféim díochlaonadh, inscne, tuiseal, agus uimhir a chur in iúl. É sin ráite, níl an ábaltacht moirféim ar leith a chuardach ar fáil ar acmhainn ar bith eile ar líne, áfach, cé gur mó an tairbhe.<br>
            Le <i>mirador</i> na Spáinne mar inspioráid, tá súil againn go dtabharfaidh an acmhainn seo stáitse nua as a bheith ag amharc ar mhíreanna éagsúla na Gaeilge. Tá suil againn go mbeidh Míreadóir úsáideach d’fhoghlaimeoirí agus do mhúinteoirí na Gaeilge, chomh maith le haistritheoirí, scríbhneoirí, agus gairmithe eile a n-úsáideann an teanga.<br><br>
            <b>Fúinn</b><br>
            Is eolaí sonraí, scríbhneoir curaclaim, agus teagascóir í Mykalin Jones/Mícheáilín Nic Sheoin. Tá a croí istigh sa Ghaeilge. <br>
            Is taighdeoir PhD agus aistritheoir í <a href="https://linktr.ee/ellencorbett">Ellen Corbett</a>. Is annamh lá nach mbíonn sí ag amharc ar fhoclóir Gaeilge.<br><br>
            """
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

# Perform search and reset buttons in columns
col1, col2 = st.columns([1, 1])
with col1:
    if st.button(get_text("search", language)):
        if not substring:
            st.error(get_text("invalid_search", language))
        else:
            result = search_words(data, substring, search_type)
            if result.empty:
                st.warning(get_text("no_results", language))
            else:
                st.write(df_to_clickable_html(result), unsafe_allow_html=True)

with col2:
    if st.button(get_text("reset", language)):
        st.experimental_rerun()

# Footer
footer_text = get_text('footer', language).replace('\n', '<br>')
st.markdown(f"<footer style='text-align: left; padding: 10px 0;'>{footer_text}</footer>", unsafe_allow_html=True)
