import string
import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_words_starting_with(letter: str) -> list:
    """
    Get words starting with a given letter from Teanglann.ie.

    Args:
        letter (str): The letter to search for.

    Returns:
        list: A list of tuples containing the word and its URL.
    """
    try:
        result = requests.get(f"https://www.teanglann.ie/en/fgb/_{letter}")
        result.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Failed to fetch words for letter '{letter}': {e}")
        return []
    soup = BeautifulSoup(result.content, "html.parser")
    samples = soup.find_all("span", class_="abcItem")
    words = [(sample.a.text, f"https://www.teanglann.ie/en/fgb/{sample.a.text}") for sample in samples]
    return words

def get_all_words() -> list:
    """
    Get all words from Teanglann.ie.

    Returns:
        list: A list of all words.
    """
    all_words = []
    letters = string.ascii_lowercase
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(get_words_starting_with, letter): letter for letter in letters}
        for future in as_completed(futures):
            try:
                words = future.result()
                all_words.extend(words)
            except Exception as e:
                print(f"Error fetching words: {e}")
    return all_words

def save_data_to_csv(data: list, filename: str):
    """
    Save data to a CSV file.

    Args:
        data (list): The data to save.
        filename (str): The path to the CSV file.
    """
    df = pd.DataFrame(data, columns=['Word', 'Link'])
    df.to_csv(filename, index=False)

# Main script
if __name__ == "__main__":
    all_words = get_all_words()
    save_data_to_csv(all_words, 'teanglann_words.csv')