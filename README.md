# Web-Scraping

The provided Python script is a Streamlit web application designed to scrape product information from Amazon based on user-selected product categories. Here's a breakdown of its functionality:

AmazonScraper Class:

Utilizes BeautifulSoup and requests libraries to scrape product information from Amazon.
Scrapes data such as product title, brand, price, rating, reviews, availability, product URL, and product details.
Implements methods to extract specific product attributes from the Amazon webpage.

Main Function (main):

Sets up the Streamlit application layout with a title and logo image.
Provides checkboxes for users to select desired product categories.
Upon clicking the "Explore Products" button, initiates the scraping process for the selected products.
Displays the scraped product data in a table format using Streamlit.
Provides a button to download the product data table as a PDF.
Overall, this script allows users to explore and analyze product information from Amazon within a Streamlit web application interface.
