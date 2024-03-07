import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import requests
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_option_menu import option_menu
from PIL import Image
import pdfkit

class AmazonScraper:
    def __init__(self, product_names):
        self.product_names = product_names
        self.headers = {'User-Agent':'', 'Accept-Language': 'en-US, en;q=0.5'}
        self.base_url = "https://www.amazon.in/s?k="
        self.links_list = self._get_links()

    def _get_links(self):
        links_list = []
        for product_name in self.product_names:
            search_url = self.base_url + product_name.replace(" ", "+")
            webpage = requests.get(search_url, headers=self.headers)
            soup = BeautifulSoup(webpage.content, "html.parser")
            links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})
            for link in links:
                if link.get('href') and '/dp/' in link.get('href'):
                    links_list.append(link.get('href'))
        return links_list

    def scrape_amazon_product_info(self):
        data = {"Product":[], "Brand":[],"Brand URL":[], "Price":[], "Rating":[], "Reviews":[], "Availability":[], 'Product URL':[], 'Product_Details':[]}
        for link in self.links_list:
            new_webpage = requests.get("https://www.amazon.in" + link, headers=self.headers)
            new_soup = BeautifulSoup(new_webpage.content, "html.parser")
            data['Product'].append(self.get_title(new_soup))
            data['Brand'].append(self.get_brand_name(new_soup))
            data['Brand URL'].append(self.get_brand_url(new_soup))
            data['Price'].append(self.get_price(new_soup))
            data['Rating'].append(self.get_rating(new_soup))
            data['Reviews'].append(self.get_review_count(new_soup))
            data['Availability'].append(self.get_availability(new_soup))
            data['Product URL'].append(self.get_url(new_soup))
            data['Product_Details'].append(self.get_prod_dim(new_soup))
        return data

    def get_title(self, soup):
        try:
            title = soup.find("span", attrs={"id":'productTitle'})
            title_value = title.text
            return title_value.strip()
        except AttributeError:
            return ""

    def get_brand_url(self, soup):       
        brand_url = ""
        brand_link = soup.find('a', {'id': 'bylineInfo'})

        if brand_link is not None and 'href' in brand_link.attrs:
            brand_url = 'https://www.amazon.com' + brand_link['href']
        
        return brand_url
 
 
    def get_brand_name(self,soup):    
        brand_element = soup.find("span", attrs={'class':'a-size-base po-break-word'})
        brand_name = brand_element.string.strip() if brand_element else ""
    #     if price == 'Page 1 of 1':
    #         price = 'NA'
        return brand_name

    def get_rating(self, soup):
        try:
            rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
            return rating
        except AttributeError:
            try:
                rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
                return rating
            except:
                return ""

    def get_review_count(self, soup):
        try:
            review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()
            return review_count
        except AttributeError:
            return ""

    def get_availability(self, soup):
        try:
            available = soup.find("div", attrs={'id':'availability'}).find("span").string.strip()
            return available
        except AttributeError:
            return "Not Available"

    def get_price(self, soup):
        try:
            price = soup.find("span", attrs={'class':'a-offscreen'}).string.strip()
            if price == 'Page 1 of 1':
                return 'NA'
            return price
        except AttributeError:
            return ""

    def get_prod_dim(self, soup):
        product_details = {}
        table = soup.find("table", {"id": "productDetails_detailBullets_sections1"})
        if table:
            rows = table.find_all("tr")
            for row in rows:
                cells = row.find_all(["th", "td"])
                if len(cells) == 2:
                    attribute = cells[0].text.strip()
                    value = cells[1].text.strip()
                    product_details[attribute] = value
        return product_details

    def get_url(self, soup):
        canonical_url = ""
        link = soup.find("link", attrs={"rel": "canonical"})
        if link and link.has_attr('href'):
            canonical_url = link['href']
        return canonical_url

def get_table_download_link(df):
    # Convert DataFrame to PDF
    pdfkit.from_file(df.to_html(), 'out.pdf')

    with open("out.pdf", "rb") as file:
        pdf_bytes = file.read()

    b64_pdf = base64.b64encode(pdf_bytes).decode()  
    href = f'<a href="data:application/octet-stream;base64,{b64_pdf}" download="products.pdf" target="_blank">Download Products as PDF</a>'
    return href

def main():
    st.set_page_config(layout="wide")
    st.markdown("""
        <style>
            .block-container {
                padding-top: 2rem;
                padding-bottom: 0rem;
                padding-left: 2.5rem;
                padding-right: 2.5rem;
            } 
            .div.css-10qvep2.e1f1d6gn1 {
                height=10px !important;
            }
        </style>
        """, unsafe_allow_html=True)

    with st.container():
        col1, col3 = st.columns([0.1,0.9],gap="small")
        with col1:
            logo_image = Image.open(r".assets/scraper.png")
            resized_logo = logo_image.resize((100, 100))
            logo_width, logo_height = resized_logo.size
            logo= st.image(resized_logo, use_column_width=False, output_format="auto", width=logo_width) 
        with col3:
            st.title("Product Scraper")
    

    products = [
        "Women Beauty Products",
        "Women Kurtis",
        "Shoes",
        "Watches",
        "Mixer Griender",
    ]
    
    with st.container():
        col1, col2,col3,col4 = st.columns(4)
        with col1:
            selected_products_col1 = []
            for product in products[:2]:
                selected = st.checkbox(product, key=product)
                if selected:
                    selected_products_col1.append(product)

        with col2:
            selected_products_col2 = []
            for product in products[2:4]:
                selected = st.checkbox(product, key=product)
                if selected:
                    selected_products_col2.append(product)
        with col3:
            selected_products_col3 = []
            for product in products[4:6]:
                selected = st.checkbox(product, key=product)
                if selected:
                    selected_products_col3.append(product)

        with col4:
            selected_products_col4 = []
            for product in products[6:8]:
                selected = st.checkbox(product, key=product)
                if selected:
                    selected_products_col4.append(product)


        selected_products = selected_products_col1 + selected_products_col2 + selected_products_col3 + selected_products_col4


        # # Display checkboxes for each product
        # selected_products = []
        # for product in products:
        #     selected = st.checkbox(product)
        #     if selected:
        #         selected_products.append(product)

        # # Display the selected products
        # st.write("Selected Products:", selected_products)
        st.markdown("""<style> 
            .stButton>button {
                    background-color: #3E3800; 
                    color: #FFFFFF;
            }</style>""", unsafe_allow_html=True)

        if st.button("Explore Products"):
            if selected_products:
                
                scraper = AmazonScraper(selected_products)
                amazon_data = scraper.scrape_amazon_product_info()
                amazon_df = pd.DataFrame.from_dict(amazon_data)
                amazon_df['Brand URL'] = amazon_df['Brand URL'].apply(lambda x: f'[{x}]({x})')
                amazon_df['Product URL'] = amazon_df['Brand URL'].apply(lambda x: f'[{x}]({x})')
                # for url, prod, brand in zip(amazon_data['Brand_url'], amazon_data['Product'], amazon_data['Brand']):
                #     st.markdown(f"[{prod} by {brand}]({url})")
                st.write(
                amazon_df
                    # .style
                    # .set_properties(**{'color': 'black', 'font-weight': 'bold'})
                    # .apply(lambda x: ['background-color: #FFE600' if x.name==amazon_df.columns else 'background-color: lightgrey' for i in x], axis=1)
                )
            else:
                st.warning("Please select at least one product.")
            # st.markdown(get_table_download_link(amazon_df), unsafe_allow_html=True)

if __name__ == "__main__":
    main()