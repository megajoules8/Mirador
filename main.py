import streamlit as st
import pandas as pd
import unicodedata
import re

def normalize_string(input_str: str) -> str:
    """
    Normalize function to remove accents and convert to lowercase.

    Args:
        input_str (str): The input string to normalize.

    Returns:
        str: The normalized string.
    """
    return ''.join(
        char for char in unicodedata.normalize('NFD', input_str)
        if unicodedata.category(char) != 'Mn'
    ).lower()

@st.cache_data
def load_data(filename: str) -> pd.DataFrame:
    """
    Load data from a CSV file, preprocess it, and sort by SortKey.

    Args:
        filename (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The preprocessed and sorted DataFrame.
    """
    df = pd.read_csv(filename)
    df['NormalizedWord'] = df['Word'].apply(normalize_string)
    df['SortKey'] = df['NormalizedWord'].str.replace('-', '', regex=False)
    return df.sort_values(by='SortKey')

def get_text(key: str, language: str) -> str:
    """
    Retrieve the text for a given key and language.

    Args:
        key (str): The key for the text.
        language (str): The language code (e.g., 'en' or 'ga').

    Returns:
        str: The text corresponding to the key and language.
    """
    language = language.lower()  # Convert to lowercase for matching dictionary keys
    texts = {
        "title": {"en": "Míreadóir: Search Irish-language Morphemes and Substrings", "ga": "Míreadóir: Cuardaigh Moirféimí agus Fotheaghráin na Gaeilge"},
        "enter_substring": {"en": "Enter substring to search:", "ga": "Cuir fotheagrán isteach chun cuardach a dhéanamh:"},
        "search_type": {"en": "Search type:", "ga": "Cineál cuardaigh:"},
        "begins_with": {"en": "Begins with", "ga": "A thosaíonn le"},
        "ends_with": {"en": "Ends with", "ga": "A chríochnaíonn le"},
        "contains": {"en": "Contains", "ga": "Áit ar bith"},
        "regex": {"en": "Regex", "ga": "Regex"},
        "search": {"en": "Search", "ga": "Cuardaigh"},
        "reset": {"en": "Reset", "ga": "Bánaigh"},
        "no_results": {"en": "No results found.", "ga": "Níor aimsíodh aon toradh."},
        "invalid_search": {"en": "Please enter a valid substring.", "ga": "Cuir cuardach bailí isteach."},
        "match_type": {"en": "Match type:", "ga": "An Sórt Meaits:"},
        "partial_match": {"en": "Partial match", "ga": "Meaits páirteach"},
        "exact_match": {"en": "Exact match", "ga": "Meaits cruinn"},
        "results_count": {"en": "Number of results:", "ga": "Líon na dtorthaí:"},
        "footer": {
            "en": """Type any part of a word you would like results for and then select if you would like results to "begin with", "contain", or "end with" those letters.<br>
            Note: Partial matches with and without sínte fada are included in the partial match results.<br><br> 
            <b>Creators</b><br>
            <u>Mykalin Jones</u>: App Development and Concept<br>
            <u>Ellen Corbett</u>: Translation and Concept<br><br>
            <b>Míreadóir</b><br>
            <i>Míreadóir</i> [Mir-a-door] aims to enable users to search for specific Irish-language morphemes including suffixes, prefixes, and other affixes. Currently it allows users to search by substring (parts of words).<br>
            Morphemes can denote declension, gender, case, and number. However, the ability to search for specific morphemes is not currently available through other online resources, despite its usefulness.<br>
            Taking inspiration from the Spanish <i>mirador</i>, we hope that this resource will provide a new vantage point from which to view Irish <i>mír</i>. We hope that Míreadóir will be useful to Irish-language learners and teachers, translators, writers, language professionals, or anyone interested in the language.<br><br>
            <b>About Us</b><br>
            <a href="https://linktr.ee/Mykalin">Mykalin Jones/Mícheáilín Nic Sheoin</a> (she/her) is a data scientist, curriculum writer, instructor, and passionate learner of the Irish language. <br>
            <a href="https://linktr.ee/ellencorbett">Ellen Corbett</a> (she/her) is a PhD researcher, translator, and frequent user of Irish dictionaries.<br><br>
            """,
            "ga": """Cuir isteach an mhoirféim nó an fotheaghrán a bhfuil tú ag iarraidh a chuardach. Roghnaigh ar 
            mhaith leat torthaí “a thosaíonn le”, nó “a chríochnaíonn le” moirféim nó fotheaghrán ar leith, 
            nó a bhfuil le feiceáil in “áit ar bith” san fhocal.<br>
            Nóta: Cuirtear meaitseanna páirteacha le agus gan shínte fada san áireamh i dtórthaí meaits páirteach<br><br>
            <b>Na Cruthaitheoirí</b><br>
            <u>Mykalin Jones</u> a d'fhobairt agus a smaoinigh ar an choincheap<br>
            <u>Ellen Corbett</u> a d'aistrigh agus a smaoinigh ar an choincheap<br><br>
            <b>Míreadóir</b><br>
            Uasdátú: Is é mar sprioc ag Míreadóir go mbeidh úsáideoirí ábalta cuardach a dhéanamh ar mhoirféim ar leith, iarmhíreanna, réimíreanna, agus táthmhíreanna eile san áireamh. Ag an bhomaite, ligeann Míreadóir d’úsáideoirí fotheaghráin [‘substrings’] a chuardach.<br>
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

def search_words(data: pd.DataFrame, substring: str, search_type: str, match_type: str, language: str) -> pd.DataFrame:
    """
    Search for words in the DataFrame based on the given substring, search type, and match type.

    Args:
        data (pd.DataFrame): The DataFrame containing the words to search.
        substring (str): The substring to search for.
        search_type (str): The type of search ('begins_with', 'ends_with', 'contains', 'regex').
        match_type (str): The type of match ('partial_match', 'exact_match').
        language (str): The language code (e.g., 'en' or 'ga').

    Returns:
        pd.DataFrame: The filtered DataFrame with the search results.
    """
    normalized_substring = normalize_string(substring) if match_type == get_text("partial_match", language) else substring

    if search_type == get_text("begins_with", language):
        filtered_data = data[data['NormalizedWord'].str.startswith(normalized_substring) if match_type == get_text("partial_match", language) else data['Word'].str.startswith(substring)]
    elif search_type == get_text("ends_with", language):
        filtered_data = data[data['NormalizedWord'].str.endswith(normalized_substring) if match_type == get_text("partial_match", language) else data['Word'].str.endswith(substring)]
    elif search_type == get_text("contains", language):
        filtered_data = data[data['NormalizedWord'].str.contains(normalized_substring, na=False) if match_type == get_text("partial_match", language) else data['Word'].str.contains(substring, na=False)]
    elif search_type == get_text("regex", language):
        try:
            filtered_data = data[data['Word'].str.contains(substring, regex=True, na=False)]
        except re.error:
            st.error("Invalid regular expression.")
            return pd.DataFrame(columns=['Word', 'Link'])
    else:
        filtered_data = pd.DataFrame(columns=['Word', 'Link'])

    return filtered_data

def df_to_clickable_html(df: pd.DataFrame) -> str:
    """
    Convert a DataFrame to HTML with clickable links.

    Args:
        df (pd.DataFrame): The DataFrame to convert.

    Returns:
        str: The HTML representation of the DataFrame with clickable links.
    """
    df['Link'] = df.apply(lambda row: f'<a href="{row["Link"]}" target="_blank">{row["Link"]}</a>', axis=1)
    return df[['Word', 'Link']].to_html(escape=False, index=False)

if __name__ == "__main__":

    # Streamlit UI
    logo = "mireadoir.png"

    # Sidebar with logo and language selection
    with st.sidebar:
        st.image(logo, width=250)
        language = st.selectbox("Roghnaigh teanga / Select Language:", ['GA', 'EN'], index=0)

        # Add a clickable link in the sidebar
        cheatsheet_urls = {
            "en": "https://clubanfhainne.wixsite.com/clubanfhainne/en/post/how-to-use-m%C3%ADreadoir-as-a-rhyming-dictionary",  # Replace with the actual English cheatsheet URL
            "ga": "https://clubanfhainne.wixsite.com/clubanfhainne/post/conas-m%C3%ADread%C3%B3ir-a-%C3%BAs%C3%A1id-mar-fhocl%C3%B3ir-r%C3%ADme"   # Replace with the actual Irish cheatsheet URL
        }

        cheatsheet_text = {
            "en": "How to use Míreadóir as a Rhyming Dictionary",
            "ga": "Conas Míreadóir a úsáid mar Fhoclóir Ríme"
        }

        st.markdown(f"""
            <p style="text-align: left;">
                <a href="{cheatsheet_urls[language.lower()]}" target="_blank" style="text-decoration: none; color: #007BFF;">
                    {cheatsheet_text[language.lower()]}
                </a>
            </p>
        """, unsafe_allow_html=True)

    # App title
    st.title(get_text("title", language))

    # Input fields
    substring = st.text_input(get_text("enter_substring", language))
    search_type = st.selectbox(get_text("search_type", language), [
        get_text("begins_with", language),
        get_text("ends_with", language),
        get_text("contains", language),
        get_text("regex", language)
    ])

    # Toggle for match type
    match_type = st.radio(get_text("match_type", language), [
        get_text("partial_match", language),
        get_text("exact_match", language)
    ])

    # Load data
    data = load_data("teanglann_words.csv")

    # Columns for search and reset buttons
    col1, col2, col3 = st.columns([3, 3, 1])
    with col1:
        if st.button(get_text("search", language)):
            if not substring.strip():
                st.error(get_text("invalid_search", language))
            else:
                try:
                    result = search_words(data, substring, search_type, match_type, language)
                    num_results = len(result)
                    if result.empty:
                        st.warning(get_text("no_results", language))
                    else:
                        st.write(f"{get_text('results_count', language)} {num_results}")
                        
                        # Add a download button for the results
                        csv = result.to_csv(index=False)
                        download_label = {
                            "en": "Download Results as CSV",
                            "ga": "Íoslódáil Torthaí mar CSV" #check this translation
                        }
                        st.download_button(
                            label=download_label[language.lower()],
                            data=csv,
                            file_name="search_results.csv",
                            mime="text/csv"
                        )
                        
                        st.write(df_to_clickable_html(result), unsafe_allow_html=True)

                        
                except re.error:
                    st.error("Invalid regular expression. Please check your input.")

    with col3:
        if st.button(get_text("reset", language)):
            st.experimental_rerun()

    # Footer
    footer_text = get_text('footer', language).replace('\n', '<br>')
    st.markdown(f"<footer style='text-align: left; padding: 10px 0;'>{footer_text}</footer>", unsafe_allow_html=True)
