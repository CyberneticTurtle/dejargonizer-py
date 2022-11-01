from lib2to3.pgen2 import token
import re
import numpy as np
import pandas as pd
from cleantext import clean
from .jargon_list import jargon_df


def strip_characters(a_string):
    """
    Remove all non-alphabetic characters (except "-") from input string.

    Args:
        a_string: Input string

    Returns:
        Input string with all non-alphabetic characters (except "-") removed
    """
    r = re.compile(r"[^a-zA-Z- ]")
    new_string = r.sub(" ", a_string)
    # In case text is left with extraneous hyphens, for example with the word
    # "3-dimensional", the above regex will convert it into "-dimensional".
    # This is problematic as the word corpus does not expect words to start
    # with a hyphen
    r = re.compile(r" -|- ")
    return r.sub(" ", new_string)


def remove_spaces(a_string):
    """
    Remove consecutive spaces and replace with single space.

    Args:
        a_string: Input string
    
    Returns:
        Input string with all consecutive spaces replaced by a single space
    """
    return re.sub(" +", " ", a_string)


def remove_apos_s(a_string):
    """
    Remove "'s" from text.

    Args:
        a_string: Input string
    
    Returns:
        Input string with all "'s"es removed
    """
    return re.sub("'s", "", a_string)


def clean_input_text(input_text):
    """
    Clean input text for processing. This function will convert all text to
    lowercase, remove "'s"es, and remove non-alphabetic characters (except "-").

    Args:
        input_text: Input text
    
    Returns:
        Cleaned input text for processing word rarity
    """
    # Clean input text (cleantext will convert to lowercase by default)
    input_text = clean(input_text)
    # Remove apostrophe-s from words
    input_text = remove_apos_s(input_text)
    # Strip non-essential characters
    input_text = strip_characters(input_text)
    # Remove internal spaces
    input_text = remove_spaces(input_text)
    # Remove end spaces
    input_text = input_text.strip()
    return input_text


def tokenize(cleaned_text):
    """
    This function tokenizes the input text. Returns a DataFrame with words and their number of
    occurrences in the input text.

    Args:
        cleaned_text: Input text cleaned with `clean_input_text()`

    Returns:
        Pandas DataFrame with columns "word" and "token_count" denoting each word and its number
        of occurrences in the input text.
    """
    # Split string on spaces and return a DataFrame of tokens and their counts
    token_set, token_counts = np.unique(cleaned_text.split(" "), return_counts=True)
    token_df = pd.DataFrame()
    token_df["word"] = token_set
    token_df["token_count"] = token_counts
    return token_df


def fetch_rarity(token_df):
    """
    Returns rarity values of each word in input text.

    Args:
        token_df: Pandas DataFrame of tokenized input text from `tokenize()`

    Returns:
        Pandas DataFrame with rarity values of each word in input text
    """
    # Easier and faster to just left-join the two DataFrames and fill empty
    # values with 0
    results = pd.merge(token_df, jargon_df, how="left", on="word")
    results = results.fillna(0)
    return results


def rare_finder(token_df, min_count, max_count):
    """
    Return rare words (between min_count and max_count) from input text.

    Args:
        token_df: Pandas DataFrame of tokenized input text from `fetch_rarity()`
        min_count: Minimum count of rare word in original corpus
        max_count: Maximum count of rare word in original corpus
    
    Returns:
        Pandas DataFrame with columns "word" and "token_count" of rare words in input text
    """
    # For a word to be rare, it either has to be within the top and bottom indices or it has a
    # count of 0
    rare_words = token_df[
        (token_df["count"] >= min_count) & (token_df["count"] <= max_count)
    ]

    return rare_words[["word", "token_count"]]


def get_jargon_words(input_text, min_count=0, max_count=80):
    """
    Return jargon words (between min_count and max_count) in input text.

    Args:
        input_text: Input text
        min_count: Minimum count for rare word in jargon corpus. Default 0
        max_count: Maximum count for rare word in jargon corpus. Default 80
    
    Returns:
        List of jargon words as tuples of (word, word_count)
    """
    cleaned_input_text = clean_input_text(input_text)
    tokens = tokenize(cleaned_input_text)
    token_values = fetch_rarity(tokens)

    rare_words = rare_finder(token_values, min_count, max_count - 1)
    return list(zip(rare_words["word"], rare_words["token_count"]))


def get_jargon_score(input_text, max_rare_count=80, max_uncommon_count=1000):
    """
    Calculate jargon score of entire input text.

    Args:
        input_text: Input text
        max_rare_count: Maximum count for rare word in jargon corpus. Default 80
        max_uncommon_count: Maximum count for uncommon word in jargon corpus. Default 1000
    
    Returns:
        Jargon score of input text. Calculated as 100 * (1 - 0.5 * uncommon words - 1 * rare words)
    """
    cleaned_input_text = clean_input_text(input_text)
    tokens = tokenize(cleaned_input_text)
    token_values = fetch_rarity(tokens)
    total_words = token_values["token_count"].sum()

    uncommon_words = rare_finder(token_values, max_rare_count, max_uncommon_count)
    rare_words = rare_finder(token_values, 0, max_rare_count - 1)

    jargon_score = 100 * (1 - 0.5 * (uncommon_words["token_count"].sum() / total_words)
        - 1 * (rare_words["token_count"].sum() / total_words))

    return jargon_score
