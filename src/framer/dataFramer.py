from collections import defaultdict, Counter
from datetime import datetime
import time
from typing import Any, Dict, List, Optional, Tuple
import pandas as pd
import re
import urllib.parse
import os
import nltk
from nltk.util import ngrams
from nltk.tokenize import word_tokenize

# Ensure NLTK data is available
nltk.download('punkt')
nltk.download('punkt_tab')


class DataFramer:
    """
    A class responsible for handling and processing data frames related to HTML elements, text analysis, and keyword extraction.

    The `DataFramer` class provides methods to clean URLs for file naming, create styled DataFrames from various types of data,
    and save these DataFrames to HTML files. It also includes functionality for tokenizing text, generating n-grams, and analyzing
    keyword frequencies. This class is useful for tasks such as data analysis, text processing, and generating HTML reports from
    structured data.

    Attributes:
        None

    Methods:
        _clean_url_for_filename(url: Optional[str]) -> str:
            Cleans a URL to create a valid file name by removing 'http://', 'www.', and domain extensions, and replacing periods
            with hyphens. If the URL is None, returns a default name.

        _create_element_details_df(data: List[Dict[str, Any]], url: Optional[str] = None) -> None:
            Creates and styles a DataFrame from the provided extracted HTML element data and saves it as an HTML file. The DataFrame
            includes columns from the dictionaries in the data list, and the resulting HTML file is saved with a name derived from
            the URL. If the URL is None, a default filename is used.

        _generate_ngrams(tokens: List[str], n: int) -> List[str]:
            Generates n-grams from a list of tokens. An n-gram is a contiguous sequence of n items from the tokens list.

        _create_word_freq_df(data: List[Dict[str, Any]], url: Optional[str] = None) -> None:
            Counts the frequency of unique n-grams (unigrams, bigrams, trigrams) found in 'TEXT' and 'ALT' values of the provided
            data and saves the counts to an HTML file. The file name is based on the URL if provided; otherwise, a default name is used.

        _create_keywords_df(keywords: Dict[str, List[Tuple[str, float]]], url: Optional[str] = None) -> None:
            Creates and saves a styled DataFrame that lists keywords and their scores for each tag type. The DataFrame is saved as
            an HTML file with a name derived from the URL. If the URL is None, a default filename is used.


    """

    def __init__(self) -> None:
        """
        Initializes the DataFramer instance. This constructor does not perform any specific initialization
        beyond the default behavior.
        """
        pass

    def _clean_url_for_filename(self, url: Optional[str]) -> str:
        """
        Cleans a URL to create a valid file name by removing 'http://', 'www.', and domain extensions,
        and replacing periods with hyphens. If the URL is None, returns a default name.

        Args:
            url (Optional[str]): The URL to be cleaned. If None, a default name is returned.

        Returns:
            str: A cleaned version of the URL suitable for file naming, or a default name if the URL is None.
        """
        if url is None:
            return "google_results"
        
        parsed_url = urllib.parse.urlparse(url)
        netloc = parsed_url.netloc
        netloc = re.sub(r'^https?://', '', netloc)
        netloc = re.sub(r'^www\.', '', netloc)
        netloc = netloc.split('.')[0]
        cleaned_filename = re.sub(r'\.', '-', netloc)
        
        if not cleaned_filename:
            cleaned_filename = "default_filename"
        
        return cleaned_filename

    def _create_element_details_df(self, data: List[Dict[str, Any]], url: Optional[str] = None) -> None:
        """
        Creates and styles a DataFrame from the provided extracted HTML element data and saves it as an HTML file.
        The DataFrame includes columns from the dictionaries in the data list, and the resulting HTML file is
        saved with a name derived from the URL.

        Args:
            data (List[Dict[str, Any]]): A list of dictionaries where each dictionary represents an HTML element.
            url (Optional[str]): The URL associated with the data. If None, a default filename is used.
        """
        df = pd.DataFrame(data)
        
        styled_df = df.style.set_table_styles([
            {'selector': 'th', 'props': [('background-color', '#4CAF50'), ('color', 'white'), ('font-weight', 'bold'), ('text-align', 'center'), ('border', '1px solid black')]},
            {'selector': 'td', 'props': [('text-align', 'left'), ('border', '1px solid black')]},
            {'selector': 'caption', 'props': [('caption-side', 'top'), ('font-size', '1.5em'), ('font-weight', 'bold'), ('color', '#333')]},
        ]).set_caption(f"HTML Element details for: {url}")

        if url:
            cleaned_url = self._clean_url_for_filename(url)
            output_filename = f"{cleaned_url}_element_details_df.html"
        else:
            output_filename = "NAME-MISSING_element_details_df.html"
        
        output_folder = f'../dataframes/{cleaned_url}'
        os.makedirs(output_folder, exist_ok=True)
        output_path = os.path.join(output_folder, output_filename)
        
        with open(output_path, "w") as file:
            file.write(styled_df.to_html())
        
        print(f"Saved DataFrame for element details as '{output_path}'")

    def _tokenize(self, text: str) -> List[str]:
        """
        Tokenizes the input text into individual words.

        Args:
            text (str): The text to be tokenized.

        Returns:
            List[str]: A list of tokens (words) obtained from the text.
        """
        return word_tokenize(text.lower())

    def _generate_ngrams(self, tokens: List[str], n: int) -> List[str]:
        """
        Generates n-grams from a list of tokens. An n-gram is a contiguous sequence of n items from the tokens list.

        Args:
            tokens (List[str]): The list of tokens to generate n-grams from.
            n (int): The length of n-grams to generate (e.g., 1 for unigrams, 2 for bigrams, etc.).

        Returns:
            List[str]: A list of n-grams represented as strings.
        """
        return [' '.join(ngram) for ngram in ngrams(tokens, n)]

    def _create_word_freq_df(self, data: List[Dict[str, Any]], url: Optional[str] = None) -> None:
        """
        Counts the frequency of unique n-grams (unigrams, bigrams, trigrams) found in 'TEXT' and 'ALT' values of
        the provided data and saves the counts to an HTML file. The file name is based on the URL if provided.

        Args:
            data (List[Dict[str, Any]]): A list of dictionaries where each dictionary contains 'TEXT' or 'ALT' values.
            url (Optional[str]): The URL associated with the data. If None, a default filename is used.
        """
        one_grams, two_grams, three_grams = [], [], []

        for item in data:
            if 'TEXT' in item:
                tokens = self._tokenize(item['TEXT'])
                one_grams.extend(self._generate_ngrams(tokens, 1))
                two_grams.extend(self._generate_ngrams(tokens, 2))
                three_grams.extend(self._generate_ngrams(tokens, 3))
            if 'ALT' in item:
                tokens = self._tokenize(item['ALT'])
                one_grams.extend(self._generate_ngrams(tokens, 1))
                two_grams.extend(self._generate_ngrams(tokens, 2))
                three_grams.extend(self._generate_ngrams(tokens, 3))

        one_gram_counts = Counter(one_grams)
        two_gram_counts = Counter(two_grams)
        three_gram_counts = Counter(three_grams)

        df_one_grams = pd.DataFrame(one_gram_counts.items(), columns=['1 Word', 'Count 1'])
        df_two_grams = pd.DataFrame(two_gram_counts.items(), columns=['2 Word', 'Count 2'])
        df_three_grams = pd.DataFrame(three_gram_counts.items(), columns=['3 Word', 'Count 3'])

        df_combined = pd.merge(
            df_one_grams[['1 Word', 'Count 1']],
            df_two_grams[['2 Word', 'Count 2']],
            how='outer',
            left_index=True,
            right_index=True
        )
        df_combined = pd.merge(
            df_combined,
            df_three_grams[['3 Word', 'Count 3']],
            how='outer',
            left_index=True,
            right_index=True
        )

        df_combined = df_combined.astype(str)
        df_combined.replace('nan', '', inplace=True)

        styled_df = df_combined.style.set_table_styles([
            {'selector': 'th', 'props': [('background-color', '#4CAF50'), ('color', 'white'), ('font-weight', 'bold'), ('text-align', 'center'), ('border', '1px solid black')]},
            {'selector': 'td', 'props': [('text-align', 'left'), ('border', '1px solid black')]},
            {'selector': 'caption', 'props': [('caption-side', 'top'), ('font-size', '1.5em'), ('font-weight', 'bold'), ('color', '#333')]},
        ]).set_caption(f"N-gram Frequency Count for: {url}")

        if url:
            cleaned_url = self._clean_url_for_filename(url)
            output_filename = f"{cleaned_url}_ngram_counts.html"
        else:
            output_filename = "MISSINGNAME_ngram_counts.html"

        output_folder = f'../dataframes/{cleaned_url}'
        os.makedirs(output_folder, exist_ok=True)

        output_path = os.path.join(output_folder, output_filename)

        with open(output_path, "w") as file:
            file.write(styled_df.to_html())

        print(f"Saved n-gram counts to '{output_path}'")

    def _create_keywords_df(self, keywords: Dict[str, List[Tuple[str, float]]], url: Optional[str] = None) -> None:
        """
        Creates and saves a styled DataFrame that lists keywords and their scores for each tag type. The DataFrame
        is saved as an HTML file with a name derived from the URL.

        Args:
            keywords (Dict[str, List[Tuple[str, float]]]): A dictionary where the key is the tag type and the value is
            a list of tuples containing keywords and their associated scores.
            url (Optional[str]): The URL associated with the data. If None, a default filename is used.
        """
        type_list, keyword_list, score_list = [], [], []

        for item_type, kws in keywords.items():
            for kw, score in kws:
                type_list.append(item_type)
                keyword_list.append(kw)
                score_list.append(score)
        
        df = pd.DataFrame({
            'Type': type_list,
            'Keyword': keyword_list,
            'Score': score_list
        })

        styled_df = df.style.set_table_styles([
            {'selector': 'th', 'props': [('background-color', '#4CAF50'), ('color', 'white'), ('font-weight', 'bold'), ('text-align', 'center'), ('border', '1px solid black')]},
            {'selector': 'td', 'props': [('text-align', 'left'), ('border', '1px solid black')]},
            {'selector': 'caption', 'props': [('caption-side', 'top'), ('font-size', '1.5em'), ('font-weight', 'bold'), ('color', '#333')]},
        ]).set_caption(f"Keywords for: {url}")

        if url:
            cleaned_url = self._clean_url_for_filename(url)
            output_filename = f"{cleaned_url}_keywords.html"
        else:
            output_filename = "MISSINGNAME_keywords.html"

        output_folder = f'../dataframes/{cleaned_url}'
        os.makedirs(output_folder, exist_ok=True)

        output_path = os.path.join(output_folder, output_filename)

        with open(output_path, "w") as file:
            file.write(styled_df.to_html())

        print(f"Saved keyword DataFrame to '{output_path}'")
