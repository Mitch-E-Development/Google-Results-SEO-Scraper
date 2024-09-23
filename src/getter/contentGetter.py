import requests
from typing import List, Dict
import time

class ContentGetter:
    """
    A class responsible for retrieving and managing HTML content from web pages and Google search results.

    The `ContentGetter` class provides methods to fetch HTML content from Google search result pages and individual
    web pages based on a list of URLs. It handles HTTP requests, manages response content, and provides functionality
    to retrieve HTTP headers for debugging and analysis. This class is useful for tasks such as content scraping, 
    data collection, and preliminary data analysis of web resources.

    Attributes:
        search_results (str): The HTML content of the Google search results page retrieved during search queries.
        page_results (List[Dict[str, str]]): A list of dictionaries where each dictionary maps a URL to its corresponding HTML content.

    Methods:
        _get_search_content(search_term: str) -> str:
            Fetches the HTML content of Google search results for the specified search term. Constructs a Google search URL, 
            sends an HTTP GET request, and retrieves the HTML content. Stores the content in the `search_results` attribute 
            and returns it. Handles request errors by printing an error message and returning an empty string.

        _get_pages_content(page_urls: List[str]) -> List[Dict[str, str]]:
            Retrieves the HTML content for a list of web page URLs. Sends HTTP GET requests to each URL and stores the HTML 
            content in a list of dictionaries, with each dictionary mapping a URL to its HTML content. Includes a delay between 
            requests to avoid overwhelming the server. Handles request errors by printing an error message and storing an empty 
            dictionary for the failed URL.

        _fetch_headers(urls: List[str]) -> None:
            Fetches and prints the HTTP headers for a list of URLs. Sends HTTP GET requests to each URL and prints the headers 
            received in the responses. Provides a clear separation in the output to distinguish headers from different URLs. 
            Handles request errors by printing an error message.

    Raises:
        requests.RequestException: This exception is raised if any error occurs during HTTP requests for fetching search 
        results, page content, or headers.
    """

    def __init__(self) -> None:
        """
        Initializes the ContentGetter instance.

        This constructor initializes the attributes:
        - `search_results` as an empty string.
        - `page_results` as an empty list.
        """
        self.search_results = ""
        self.page_results = []

    def _get_search_content(self, search_term: str) -> str:
        """
        Fetches the HTML content of Google search results for a specified search term.

        This method constructs a Google search URL with the provided search term, sends an HTTP GET request to the URL,
        and retrieves the HTML content of the search results page. If the request is successful, the HTML content is stored
        and returned. If there is an error during the request, an empty string is returned.

        Args:
            search_term (str): The search term to use in the Google search query.

        Returns:
            str: The HTML content of the search results page. Returns an empty string if an error occurs during the request.

        Raises:
            requests.RequestException: If an error occurs while making the HTTP request.
        """
        try:
            search_url = f"https://www.google.com/search?q={search_term}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
            }
            response = requests.get(search_url, headers=headers, timeout=10)
            response.raise_for_status()

            self.search_results = response.content  # Store HTML content

            return self.search_results  # Return the HTML content
            
        except requests.RequestException as e:
            print(f"Error fetching search results: {e}")
            return ""

    def _get_pages_content(self, page_urls: List[str]) -> List[Dict[str, str]]:
        """
        Fetches the HTML content of multiple web pages based on their URLs.

        This method iterates over the provided list of URLs, sends HTTP GET requests to each URL, and retrieves the HTML
        content of each page. The results are stored in a list of dictionaries where each dictionary maps a URL to its HTML content.
        To prevent overwhelming the server, there is a delay between requests. If a request fails, an empty dictionary is used
        for that URL.

        Args:
            page_urls (List[str]): A list of URLs for which to fetch the HTML content.

        Returns:
            List[Dict[str, str]]: A list of dictionaries where each dictionary maps a URL to its HTML content.

        Raises:
            requests.RequestException: If an error occurs while making the HTTP request for any URL.
        """
        page_contents = []

        for url in page_urls:
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()

                result = {url: response.content}
                page_contents.append(result)
                
                time.sleep(3)  # Delay to avoid sending too many requests in a short period
            
            except requests.RequestException as e:
                print(f"Error fetching page {url}: {e}")
                result = {url: ""}
                page_contents.append(result)

        self.page_results = page_contents
        return self.page_results

    def _fetch_headers(self, urls: List[str]) -> None:
        """
        Fetches and prints the HTTP headers of the given URLs.

        This method sends HTTP GET requests to each URL in the provided list and prints the HTTP headers received in
        the responses. The headers for each URL are printed with a clear separation to make them easy to distinguish.

        Args:
            urls (List[str]): A list of URLs for which to fetch and print HTTP headers.

        Returns:
            None: This method does not return any value. It prints the headers directly to the console.

        Raises:
            requests.RequestException: If an error occurs while making the HTTP request for any URL.
        """
        for url in urls:
            try:
                response = requests.get(url, timeout=30)
                print(f"\n\n\nHeaders for {url}:")
                print("-" * 70)
                for header, value in response.headers.items():
                    print(f"{header}: {value}")
                print("-" * 70)
            
            except requests.RequestException as e:
                print(f"Error fetching headers from {url}: {e}")
