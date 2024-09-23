import re
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Set, Tuple
from yake import KeywordExtractor
from urllib.parse import urljoin, urlparse, urlunparse

class DataExtractor:
    """
    A class responsible for extracting and analyzing various types of data from HTML content.

    The `DataExtractor` class provides methods to parse HTML documents and extract SEO-relevant information, 
    metadata, URLs, keywords, and other content-based insights. It supports the extraction of various data elements 
    such as text content from HTML tags, alt attributes from images, and structured metadata. This class is useful 
    for tasks related to SEO analysis, content scraping, and data mining from web pages.

    Attributes:
        search_data (Dict): A dictionary to store search-related data collected during extraction.
        page_data (List): A list to store data specific to individual pages, such as meta information and extracted content.

    Methods:
        _extract_page_elements(search_results: str) -> List[Dict[str, Any]]:
            Extracts SEO-relevant data from the provided HTML content by parsing various HTML tags.
        
        _extract_data_from_element(soup: BeautifulSoup, tag: str) -> List[Dict[str, Any]]:
            Extracts data from specific HTML tags within the provided BeautifulSoup object, including class names, 
            text content, and attributes.
        
        _extract_alt_text_data(tag: str, tag_classes_str: str, id: str, alt_text: str, text: str) -> Dict[str, Any]:
            Extracts and formats data specifically from 'img' tags, including alt text.
        
        _extract_text_data(tag: str, tag_classes_str: str, id: str, alt_text: str, text: str) -> Dict[str, Any]:
            Extracts and formats data from HTML tags other than 'img', focusing on text content.
        
        _extract_questions_from_elements(search_elements: List[Dict[str, Any]]) -> Dict[str, List[str]]:
            Identifies and extracts unique questions from the 'TEXT' and 'ALT' fields of HTML elements.
        
        _extract_related_search_terms(search_elements: List[Dict[str, Any]]) -> Dict[str, List[str]]:
            Extracts potential related search terms from elements with specific class names.
        
        _extract_people_also_asked(search_elements: List[Dict[str, Any]]) -> Dict[str, List[str]]:
            Extracts questions from the 'People Also Asked' section of search results based on specific class names.
        
        _extract_and_format_urls(search_data: str) -> List[str]:
            Extracts, normalizes, and formats URLs from the provided HTML content.
        
        _extract_href_urls(search_data: str) -> Set[str]:
            Extracts unique absolute URLs from the 'href' attributes of <a> tags in the HTML content.
        
        _extract_page_meta(page_content: str) -> List[Dict[str, Any]]:
            Extracts metadata information such as title and description from the provided HTML content.
        
        _extract_keywords_by_tag(search_data: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, float]]]:
            Extracts keywords from different HTML tag types using the YAKE keyword extraction algorithm.
        
        _extract_keywords_by_component(search_data: List[Dict[str, Any]]) -> Dict[str, List[Tuple[str, float]]]:
            Extracts and organizes keywords by different page components using YAKE, analyzing text from various components.
    """
    def __init__(self) -> None:
        """
        Initializes a new instance of the DataExtractor class.

        This class is responsible for extracting various types of data from HTML content,
        including SEO-related information, metadata, URLs, and keywords.

        Attributes:
            search_data (Dict): A dictionary to store search-related data collected during extraction.
            page_data (List): A list to store data specific to individual pages, such as meta information and extracted content.
        """
        self.search_data = {}
        self.page_data = []

    def _extract_page_elements(self, search_results: str) -> List[Dict[str, Any]]:
        """
        Extracts SEO-relevant data from the provided HTML content.

        This method parses the given HTML content to extract text and attributes from various HTML tags. 
        The tags are filtered based on predefined criteria to collect relevant data including text and alt attributes.

        Args:
            search_results (str): A string containing the HTML content to be parsed.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries where each dictionary represents an HTML tag 
            and includes its type, class names, id, alt attribute (for 'img' tags), and text content.
        """
        soup = BeautifulSoup(search_results, "html.parser")
        tags = [
            'title', 'meta', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'p', 'span', 'div', 'img', 'head'
        ]

        results = []
        for tag in tags:
            results.extend(self._extract_data_from_element(soup, tag)) 

        return results
    
    def _extract_data_from_element(self, soup: BeautifulSoup, tag: str) -> List[Dict[str, Any]]:
        """
        Extracts data from specific HTML tags within the provided BeautifulSoup object.

        This method collects information from all elements of a given tag type, including class names, 
        text content, and attributes. Special handling is applied for 'img' tags to include the alt attribute.

        Args:
            soup (BeautifulSoup): A BeautifulSoup object containing the parsed HTML content.
            tag (str): The type of HTML tag to extract data from (e.g., 'a', 'img', 'p').

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing the extracted data for each tag, 
            including 'TYPE', 'CLASS', 'ID', 'ALT' (for 'img' tags), and 'TEXT'.
        """
        results = []
        elements = soup.find_all(tag)
        
        for element in elements:
            tag_classes_str = " ".join(element.get("class", []))
            text = element.get_text(strip=True)
            alt_text = element.get('alt', '').strip()
            id = element.get('id', '').strip()

            if tag_classes_str or id:
                if tag == 'img':
                    results.append(self._extract_alt_text_data(tag, tag_classes_str, id, alt_text, text))
                else:
                    results.append(self._extract_text_data(tag, tag_classes_str, id, alt_text, text))
    
        return results

    def _extract_alt_text_data(self, tag: str, tag_classes_str: str, id: str, alt_text: str, text: str) -> Dict[str, Any]:
        """
        Extracts and formats data specifically from 'img' tags.

        This method handles the extraction of information from 'img' tags, including alt text, 
        which is relevant for SEO purposes.

        Args:
            tag (str): The HTML tag ('img').
            tag_classes_str (str): The class attribute of the 'img' tag.
            id (str): The id attribute of the 'img' tag.
            alt_text (str): The alt attribute of the 'img' tag.
            text (str): The text content of the 'img' tag (usually empty).

        Returns:
            Dict[str, Any]: A dictionary containing the extracted data, with keys 'TYPE', 'CLASS', 'ID', 'ALT', and 'TEXT'.
        """
        if alt_text:
            return {"TYPE": tag, "CLASS": tag_classes_str, "ID": id, "ALT": alt_text, "TEXT": text}
        return {"TYPE": tag, "CLASS": tag_classes_str, "ID": id, "ALT": '', "TEXT": text}

    def _extract_text_data(self, tag: str, tag_classes_str: str, id: str, alt_text: str, text: str) -> Dict[str, Any]:
        """
        Extracts and formats data from HTML tags other than 'img'.

        This method is used for extracting text content from various HTML tags, handling text attributes and optional attributes.

        Args:
            tag (str): The HTML tag type (e.g., 'p', 'a', 'h1').
            tag_classes_str (str): The class attribute of the tag.
            id (str): The id attribute of the tag.
            alt_text (str): The alt attribute of the tag (empty for non-'img' tags).
            text (str): The text content of the tag.

        Returns:
            Dict[str, Any]: A dictionary containing the extracted data, including 'TYPE', 'CLASS', 'ID', 'ALT', and 'TEXT'.
        """
        if text:
            return {"TYPE": tag, "CLASS": tag_classes_str, "ID": id, "ALT": alt_text, "TEXT": text}
        return {"TYPE": tag, "CLASS": tag_classes_str, "ID": id, "ALT": alt_text, "TEXT": ''}

    def _extract_questions_from_elements(self, search_elements: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """
        Identifies and extracts unique questions from the 'TEXT' and 'ALT' fields of HTML elements.

        This method uses a regex pattern to find and collect questions from the content and alt attributes of HTML elements.

        Args:
            search_elements (List[Dict[str, Any]]): A list of dictionaries representing HTML elements with various attributes.

        Returns:
            Dict[str, List[str]]: A dictionary with a key 'questions' containing a sorted list of unique questions extracted.
        """
        question_pattern = re.compile(r'\b[A-Z][^.?!]*\?\b', re.DOTALL)
        unique_questions = set()

        for element in search_elements:
            if 'TEXT' in element:
                text = element['TEXT']
                questions = question_pattern.findall(text)
                unique_questions.update([q.strip() for q in questions if q.strip()])
            
            if 'ALT' in element:
                alt = element['ALT']
                questions = question_pattern.findall(alt)
                unique_questions.update([q.strip() for q in questions if q.strip()])

        return {'questions': sorted(unique_questions)}

    def _extract_related_search_terms(self, search_elements: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """
        Extracts potential related search terms from elements with a specific class.

        This method looks for specific class names associated with related search terms and gathers them into a list.

        Args:
            search_elements (List[Dict[str, Any]]): A list of dictionaries representing HTML elements.

        Returns:
            Dict[str, List[str]]: A dictionary with a key 'related_terms' containing a list of related search terms.
        """
        related_terms = []
        
        for element in search_elements:
            if element.get('CLASS') == 'Xe4YD':
                text_value = element.get('TEXT')
                if text_value:
                    related_terms.append(text_value)
        
        return {'related_terms': related_terms}

    def _extract_people_also_asked(self, search_elements: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """
        Extracts questions from the 'People Also Asked' section of the search results.

        This method identifies and collects unique questions from specific classes associated with the 'People Also Asked' section.

        Args:
            search_elements (List[Dict[str, Any]]): A list of dictionaries representing HTML elements.

        Returns:
            Dict[str, List[str]]: A dictionary with a key 'people_also_asked' containing a list of unique questions.
        """
        people_also_asked = {'people_also_asked': []}

        for element in search_elements:
            class_name = element.get('CLASS')
            text_value = element.get('TEXT')

            if text_value:
                if class_name in ['JCzEY tNxQIb', 'fLtXsc iIWm4b']:
                    if text_value not in people_also_asked['people_also_asked']:
                        people_also_asked['people_also_asked'].append(text_value)

        return people_also_asked

    def _extract_and_format_urls(self, search_data: str) -> List[str]:
        """
        Extracts, normalizes, and formats URLs from the provided HTML content.

        This method parses HTML to locate URLs in specific tags and classes, normalizes them, and returns a list of unique URLs.

        Args:
            search_data (str): A string containing the HTML content to be parsed.

        Returns:
            List[str]: A list of unique, normalized URLs extracted from the HTML content.
        """
        soup = BeautifulSoup(search_data, 'html.parser')
        url_classes = ['ob9lvb', 'sCuL3', 'BNeawe UPmit AP7Wnd lRVwie']
        tags = ['div', 'span']
        urls = set()
        
        for tag in tags:
            for url_class in url_classes:
                elements = soup.find_all(tag, class_=url_class)
                for element in elements:
                    text = element.get_text(strip=True)
                    text = text.replace(' › ', '/').strip()
                    text = text.replace(' ', '-').strip()
                    
                    if not text.startswith(('http://', 'https://')):
                        text = 'http://' + text
                    
                    urls.add(text.lower())

        return list(urls)

    def _extract_href_urls(self, search_data: str) -> Set[str]:
        """
        Extracts unique absolute URLs from the 'href' attributes of <a> tags.

        This method parses the HTML content to find all anchor tags, extracting and normalizing the URLs from their 'href' attributes.

        Args:
            search_data (str): A string containing the HTML content of the page.

        Returns:
            Set[str]: A set of unique absolute URLs extracted from the 'href' attributes.
        """
        soup = BeautifulSoup(search_data, 'html.parser')
        unique_hrefs = set()
        url_pattern = re.compile(r'url=([^&]+)')

        for a in soup.find_all('a', href=True):
            href = a.get('href')
            if href:
                match = url_pattern.search(href)
                if match:
                    extracted_url = match.group(1)
                    unique_hrefs.add(extracted_url)
                else:
                    parsed_url = urlparse(href)
                    if parsed_url.scheme and parsed_url.netloc:
                        unique_hrefs.add(href)

        return unique_hrefs

    def _extract_page_meta(self, page_content: str) -> List[Dict[str, Any]]:
        """
        Extracts metadata information such as title and description from the provided HTML content.

        This method retrieves the title and meta description from the HTML content and returns them in a structured format.

        Args:
            page_content (str): A string containing the HTML content of the page.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing 'Title' and 'Description' of the page.
        """
        page_meta = []
        soup = BeautifulSoup(page_content, 'html.parser')

        title = soup.title.string if soup.title else 'No title'
        description = soup.find('meta', attrs={'name': 'description'})
        description_content = description['content'] if description else 'No description'

        page_meta.append({
            "Title": title.strip(),
            "Description": description_content.strip()
            })

        return page_meta

    def _extract_keywords_by_tag(self, search_data: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, float]]]:
        """
        Extracts keywords from different HTML tag types using the YAKE keyword extraction algorithm.

        This method processes the extracted data to identify and score keywords for each tag type (e.g., 'title', 'meta', 'img').

        Args:
            search_data (List[Dict[str, Any]]): A list of dictionaries containing SEO-relevant data with various tag types.

        Returns:
            Dict[str, List[Dict[str, float]]]: A dictionary where each key is a tag type and each value is a list of dictionaries
            with keywords and their relevance scores.
        """
        keywords_by_tag = {}

        for element in search_data:
            tag_type = element.get('TYPE')
            if tag_type == 'img':
                text_content = element.get('ALT', '')
            else:
                text_content = element.get('TEXT', '')

            if not text_content.strip():
                continue

            extractor = KeywordExtractor()
            keywords = extractor.extract_keywords(text_content)
            
            if tag_type not in keywords_by_tag:
                keywords_by_tag[tag_type] = []

            for keyword, score in keywords:
                keywords_by_tag[tag_type].append({'keyword': keyword, 'score': score})

        return keywords_by_tag

    def _extract_keywords_by_component(self, search_data: List[Dict[str, Any]]) -> Dict[str, List[Tuple[str, float]]]:
        """
        Extracts and organizes keywords by different page components using YAKE.

        This method analyzes text from various components (e.g., title, meta tags, links, headings) to extract and score keywords.

        Args:
            search_data (List[Dict[str, Any]]): A list of dictionaries containing SEO-relevant data categorized by different HTML components.

        Returns:
            Dict[str, List[Tuple[str, float]]]: A dictionary where each key represents a page component and each value is a list of tuples
            containing keywords and their relevance scores, filtered and sorted by relevance.
        """
        extractor = KeywordExtractor()
        categories = {
            'title_kws': [],
            'meta_kws': [],
            'link_kws': [],
            'heading_kws': [],
            'content_body_kws': [],
            'img_alt_kws': [],
            'questions_kws': [],
            'other_kws': []
        }

        for item in search_data:
            item_type = item.get("TYPE")
            text_content = item.get("TEXT", "")

            if item_type == 'title':
                categories['title_kws'].append(text_content)
            elif item_type == 'meta':
                categories['meta_kws'].append(text_content)
            elif item_type == 'a':
                categories['link_kws'].append(text_content)
            elif item_type in ['h1', 'h2', 'h3', 'h4', 'h5']:
                categories['heading_kws'].append(text_content)
            elif item_type in ['div', 'span', 'p', 'section', 'article']:
                categories['content_body_kws'].append(text_content)
            elif item_type == 'img':
                categories['img_alt_kws'].append(item.get("ALT", ""))
            else:
                categories['other_kws'].append(text_content)

        extracted_keywords = {}
        for key, texts in categories.items():
            combined_text = " ".join(texts)
            if combined_text.strip():
                extracted_keywords[key] = extractor.extract_keywords(combined_text)
            else:
                continue

        relevance_threshold = 0.0009
        filtered_keywords_by_category = {}
        for category, keywords in extracted_keywords.items():
            filtered_keywords = [kw for kw in keywords if kw[1] > relevance_threshold]
            sorted_keywords = sorted(filtered_keywords, key=lambda x: x[1], reverse=True)
            filtered_keywords_by_category[category] = sorted_keywords

        return filtered_keywords_by_category
