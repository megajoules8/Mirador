import pandas as pd
import pytest
from main import normalize_string, load_data, get_text, search_words, df_to_clickable_html


def test_normalize_string():
    """
    Test the normalize_string function.
    """
    assert normalize_string("Café") == "cafe"
    assert normalize_string("Míreadóir") == "mireadoir"
    assert normalize_string("abc123") == "abc123"
    assert normalize_string("ÁÉÍÓÚáéíóú") == "aeiouaeiou"

def test_load_data():
    """
    Test the load_data function.
    """

    # Create a sample CSV file for testing
    data = {
        "Word": ["faoí", "Árdrí", "café", "naïve"],
        "Link": ["link1", "link2", "link3", "link4"]
    }
    df = pd.DataFrame(data)
    df.to_csv("test_teanglann_words.csv", index=False)

    # Load the data using the load_data function
    loaded_df = load_data("test_teanglann_words.csv")

    # Check if the normalized columns are correctly added
    assert "NormalizedWord" in loaded_df.columns
    assert "SortKey" in loaded_df.columns
    assert loaded_df["NormalizedWord"].tolist() == ["ardri", "cafe", "faoi", "naive"]
    assert loaded_df["SortKey"].tolist() == ["ardri", "cafe", "faoi", "naive"]



def test_get_text():
    """
    Test the get_text function.
    """
    assert get_text("title", "en") == "Míreadóir: Search Irish-language Morphemes and Substrings"
    assert get_text("title", "ga") == "Míreadóir: Cuardaigh Moirféimí agus Fotheaghráin na Gaeilge"
    assert get_text("invalid_search", "en") == "Please enter a valid substring."
    assert get_text("invalid_search", "ga") == "Cuir cuardach bailí isteach."


@pytest.fixture
def mock_get_text(mocker):
    """
    Mock the get_text function.
    """
    mocker.patch("main.get_text", side_effect=lambda key, lang: {
        "partial_match": "Partial match",
        "exact_match": "Exact match",
        "begins_with": "Begins with",
        "ends_with": "Ends with",
        "contains": "Contains",
    }.get(key))

def test_search_words(mock_get_text):
    """
    Test the search_words function.
    """

    # Mock data
    data = pd.DataFrame({
        "Word": ["Míreadóir", "Fón", "Árthach"],
        "NormalizedWord": ["mireadoir", "fon", "arthach"],
        "SortKey": ["mireadoir", "fon", "arthach"]
    })

    # Test 'contains' with partial match
    result = search_words(data, "ír", "Contains", "Partial match", "en")
    assert len(result) == 1
    assert result.iloc[0]["Word"] == "Míreadóir"

    # Test 'begins_with' with partial match
    result = search_words(data, "F", "Begins with", "Partial match", "en")
    assert len(result) == 1
    assert result.iloc[0]["Word"] == "Fón"

    # Test 'ends_with' with partial match
    result = search_words(data, "ch", "Ends with", "Partial match", "en")
    assert len(result) == 1
    assert result.iloc[0]["Word"] == "Árthach"

    # Test no matches
    result = search_words(data, "xyz", "Contains", "Partial match", "en")
    assert len(result) == 0



def test_df_to_clickable_html():
    """
    Test the df_to_clickable_html function.
    """
    data = pd.DataFrame({
        "Word": ["Míreadóir", "Fón"],
        "Link": ["http://example.com/1", "http://example.com/2"]
    })

    html = df_to_clickable_html(data)
    assert "http://example.com/1" in html
    assert "Míreadóir" in html
    assert "<a href=" in html
