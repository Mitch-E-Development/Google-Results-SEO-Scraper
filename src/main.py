from getter.contentGetter import ContentGetter
from extractor.dataExtractor import DataExtractor
from framer.dataFramer import DataFramer


def print_dictionary(d, level=0):
    """
    Recursively prints the contents of a dictionary in a readable format.

    Args:
        d (dict): The dictionary to print.
        level (int): The current depth level for indentation.

    Returns:
        None
    """
    indent = '  ' * level
    if isinstance(d, dict):
        if not d:
            print(f"{indent}Empty dictionary.")
        for key, value in d.items():
            if isinstance(value, dict):
                print(f"{indent}{key}:")
                print_dictionary(value, level + 1)
            elif isinstance(value, list):
                print(f"{indent}{key}:")
                for item in value:
                    if isinstance(item, dict):
                        print_dictionary(item, level + 1)
                    else:
                        print(f"{indent}  - {item}")
            else:
                print(f"{indent}{key}: {value}")
    else:
        print(f"{indent}{d}")

def main():
    """
    Main function to execute the complete workflow for fetching, extracting, and processing data from Google search results and competitor web pages.

    This function orchestrates the following tasks:
    
    1. **Instantiation of Classes**: Initializes instances of `ContentGetter`, `DataExtractor`, and `DataFramer` classes to handle content retrieval, data extraction, and DataFrame creation, respectively.

    2. **User Interaction**: Prompts the user to enter a search term or type "exit" to quit. This search term is used to fetch Google search results.

    3. **Fetching Google Search Content**: Retrieves the HTML content of Google search results based on the provided search term using the `ContentGetter` instance. Handles exceptions and prints errors if content retrieval fails.

    4. **Extracting Data from Search Results**: Uses the `DataExtractor` instance to extract relevant data from the search results. This includes:
       - **Page Elements**: Extracts various elements from the search results page.
       - **Questions**: Identifies questions from the search results.
       - **Related Search Terms**: Extracts related search terms from the search results.
       - **People Also Asked**: Extracts questions from the 'People Also Asked' section.
       - **Keywords**: Extracts keywords from different components of the search results page.

    5. **Creating DataFrames for Google Search Data**: Uses the `DataFramer` instance to create and save styled DataFrames that include:
       - **Element Details**: DataFrame of HTML element details.
       - **Word Frequency**: DataFrame of word frequency counts including unigrams, bigrams, and trigrams.
       - **Keywords**: DataFrame of extracted keywords and their scores.
       - **Element Questions**: DataFrame of questions extracted from search result elements.
       - **Related Search Terms**: DataFrame of related search terms.
       - **People Also Asked**: DataFrame of questions from the 'People Also Asked' section.

    6. **Extracting URLs from Search Results**: Extracts URLs from the search results which link to competitor pages. Uses these URLs to fetch competitor page content.

    7. **Fetching Competitor Page Content**: Retrieves the HTML content of the competitor pages using the `ContentGetter` instance.

    8. **Extracting Competitor Page Data**: Uses the `DataExtractor` instance to process competitor page content, including:
       - **Page Elements**: Extracts various elements from competitor pages.
       - **Page Meta Information**: Extracts metadata such as titles and descriptions from competitor pages.
       - **Questions**: Identifies questions from competitor pages.
       - **Keywords**: Extracts keywords from different components of competitor pages.

    9. **Creating DataFrames for Competitor Page Data**: Uses the `DataFramer` instance to create and save styled DataFrames for competitor page data:
       - **Element Details**: DataFrame of HTML element details from competitor pages.
       - **Word Frequency**: DataFrame of word frequency counts from competitor pages.
       - **Page Meta Information**: DataFrame of metadata information from competitor pages.
       - **Keywords**: DataFrame of extracted keywords from competitor pages.
       - **Element Questions**: DataFrame of questions from competitor pages.

    The workflow is interactive and continues to prompt the user for new search terms until "exit" is typed. Error handling is implemented to manage exceptions that may occur during each stage of the process.

    Returns:
        None: This function runs in an interactive loop, performing data operations and handling user input. It does not return any value.

    Raises:
        Exception: Handles and prints any unexpected errors that occur during the execution of the workflow.
    """
    # Instantiate classes
    getter = ContentGetter()
    extractor = DataExtractor()
    framer = DataFramer()

    while True:
        try:
            # Getting search term from user
            search_term = input('Enter a focus keyword/search term (or type "exit" to quit): ')
            if search_term.lower() == 'exit':
                break

            # Getting Google search content
            try:
                search_results = getter._get_search_content(search_term)
                print()
            except Exception as e:
                print(f"Error getting search content: {e}")
                continue

            # Extracting data from Google search results
            try:
                search_elements = extractor._extract_page_elements(search_results)
                search_element_questions = extractor._extract_questions_from_elements(search_elements)
                related_search_terms = extractor._extract_related_search_terms(search_elements)
                people_also_asked = extractor._extract_people_also_asked(search_elements)
                search_keywords_by_component = extractor._extract_keywords_by_component(search_elements)
            except Exception as e:
                print(f"Error extracting data: {e}")
                continue

            # Creating DataFrames for Google search data
            try:
                framer._create_element_details_df(search_elements, f'http://www.google.com/search?q={search_term}')
                framer._create_word_freq_df(search_elements, f'http://www.google.com/search?q={search_term}')
                framer._create_keywords_df(search_keywords_by_component, f'http://www.google.com/search?q={search_term}')
                framer._create_element_questions_df(search_element_questions, f'http://www.google.com/search?q={search_term}')
                framer._create_related_search_terms_df(related_search_terms, f'http://www.google.com/search?q={search_term}')
                framer._create_people_also_asked_df(people_also_asked, f'http://www.google.com/search?q={search_term}')
            except Exception as e:
                print(f"Error creating DataFrames for Google search data: {e}")
                continue

            # Getting URLs for result pages
            try:
                result_urls = extractor._extract_and_format_urls(search_results)
                # result_hrefs = extractor._extract_href_urls(search_results)
                # headers = getter._fetch_headers(result_hrefs)
            except Exception as e:
                print(f"Error extracting URLs:{e}")
                continue

            # Getting competitor page content
            try:
                pages = getter._get_pages_content(result_urls)
            except Exception as e:
                print(f"Error getting competitor page content: {e}")
                continue

            # Extracting competitor page data
            try:
                for page in pages:
                    for url, page_content in page.items(): 
                        page_elements = extractor._extract_page_elements(page_content)
                        page_meta = extractor._extract_page_meta(page_content)
                        page_element_questions = extractor._extract_questions_from_elements(page_elements)
                        page_keywords_by_component = extractor._extract_keywords_by_component(page_elements)

                        # Creating DataFrames for competitor page data
                        framer._create_element_details_df(page_elements, url)
                        framer._create_word_freq_df(page_elements, url)
                        framer._create_page_meta_df(page_meta, url)
                        framer._create_keywords_df(page_keywords_by_component, url)
                        framer._create_element_questions_df(page_element_questions, url)
                        

            except Exception as e:
                print(f"Error extracting competitor page data: {e}")
                continue

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
