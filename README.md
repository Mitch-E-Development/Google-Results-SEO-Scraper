# 🌐 Google Search SEO Scraper

## 📋 Overview

This Python-based tool is designed to fetch, analyze, and process web content. It retrieves search results from Google, extracts relevant data from those results and competitor web pages, and creates detailed reports in HTML format. The tool leverages web scraping and data processing techniques to deliver insights into web content, including keywords, page elements, and meta information.

## ✨ Features

- **🔍 Google Search Content Retrieval:** Fetches HTML content from Google search results for a given search term.
- **📊 Data Extraction:**
  - Extracts HTML elements, questions, related search terms, and 'People Also Asked' sections from Google search results.
  - Retrieves and processes competitor page content, including meta information and page elements.
- **📈 Data Processing and Reporting:**
  - Creates and styles DataFrames with details about page elements, word frequencies, and keywords.
  - Saves processed data as HTML files for easy review and analysis.

## 🧩 Components

1. **ContentGetter:** Handles HTTP requests to fetch HTML content from Google search results and individual web pages.
2. **DataExtractor:** Extracts and processes relevant data from HTML content, including search results and competitor pages.
3. **DataFramer:** Creates and saves styled DataFrames from extracted data, including element details, word frequencies, and keywords.

## 🚀 Installation

To use this tool, follow these steps:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Mitch-E-Development/Web-Scrapers.git
   cd google-seo-scraper
   ```

2. **Set Up a Virtual Environment:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

3. **Install Required Packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK Data:**

   NOTE: This should be done automatically when running the scraper as long as the requirements are installed.
   
   Run the following script to download necessary NLTK data:

   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('punkt_tab')
   ```

## 🖥️ Usage

1. **Run the Main Script:**

   Execute the script to start the tool:

   ```bash
   python main.py
   ```

2. **Interactive Workflow:**

   - Enter a search term when prompted.
   - The tool will fetch Google search results, extract data, and process it.
   - It will generate and save HTML reports in the `../dataframes/` directory.
   - To analyze competitor pages, the tool will extract URLs from search results, fetch their content, and create additional reports.

3. **Terminate the Process:**

   Type `"exit"` when prompted for a new search term to quit the interactive loop.

## 📁 File Structure

- `getter/contentGetter.py`: Contains the `ContentGetter` class for retrieving HTML content.
- `extractor/dataExtractor.py`: Contains the `DataExtractor` class for extracting data from HTML content.
- `framer/dataFramer.py`: Contains the `DataFramer` class for creating and saving DataFrames.
- `main.py`: The main script that orchestrates the data extraction and processing workflow.
- `requirements.txt`: Lists the Python packages required for the project.

## 📊 Example Output

The tool generates HTML reports such as:

- `google_results_element_details_df.html`
- `google_results_ngram_counts.html`
- `google_results_keywords.html`
- `competitor_page_element_details_df.html`
- `competitor_page_meta_info_df.html`

These files are saved in the `../dataframes/` directory and include styled tables with extracted data.

## 🔧 Troubleshooting

- **Issues Fetching Data:** Ensure that the URLs and search terms are correct. Check your internet connection and ensure that Google search results are accessible.
- **Missing Libraries:** Verify that all required packages are installed and NLTK data is downloaded.


Made with ❤️ by Mitch Edmunds
