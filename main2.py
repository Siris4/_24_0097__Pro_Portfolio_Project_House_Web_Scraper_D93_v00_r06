import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import re
import time

class ZillowScraper:
    def __init__(self, url, max_scrolls=20, scroll_increment=500, scroll_pause_time=3):
        # Initialization parameters
        self.url = url
        self.max_scrolls = max_scrolls
        self.scroll_increment = scroll_increment
        self.scroll_pause_time = scroll_pause_time
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.properties = []

    def load_page(self):
        """Load the Zillow page."""
        print("Loading Zillow page...")
        self.driver.get(self.url)
        time.sleep(5)  # Give time for the page to fully load

    def scroll_page(self):
        """Scroll through the page incrementally to load more listings."""
        print("Starting to scroll the page...")
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        for scroll_count in range(1, self.max_scrolls + 1):
            self.driver.execute_script(f"window.scrollBy(0, {self.scroll_increment});")
            time.sleep(self.scroll_pause_time)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            print(f"Scroll {scroll_count}/{self.max_scrolls}")

            # Stop scrolling if no new content loads
            if new_height == last_height:
                print("Reached the end of the page.")
                break
            last_height = new_height

    def extract_page_text(self):
        """Extract text from the fully loaded page."""
        print("Extracting page text...")
        page_text = self.driver.find_element(By.TAG_NAME, 'body').text
        print("Page text extracted.")
        return page_text

    def parse_listings(self, page_text):
        """Parse the listings using regex to extract the data."""
        print("Parsing listings from the page text...")
        property_pattern = re.compile(r'([^\n]+SC \d{5})\n.*\n\$(\d{1,3}(?:,\d{3})*)\n(\d+) bds(\d+) ba([\d,]+) sqft')
        matches = property_pattern.findall(page_text)

        for i, match in enumerate(matches, start=1):
            address, price, beds, baths, sqft = match
            price = int(price.replace(',', ''))
            sqft = int(sqft.replace(',', ''))
            self.properties.append({
                'address': address,
                'price': price,
                'beds': int(beds),
                'baths': int(baths),
                'sqft': sqft
            })
        print(f"Parsed {len(self.properties)} listings.")

    def create_dataframe(self):
        """Create a pandas DataFrame from the listings."""
        print("Creating a DataFrame from the listings...")
        df = pd.DataFrame(self.properties)
        return df

    def filter_dataframe(self, df):
        """Filter the DataFrame based on the criteria."""
        print("Filtering listings (min 2 beds, min 1250 sqft)...")
        filtered_df = df[(df['beds'] >= 2) & (df['sqft'] >= 1250)]
        return filtered_df

    def close(self):
        """Close the WebDriver."""
        print("Closing the WebDriver...")
        self.driver.quit()

    def scrape(self):
        """Main scraping method to run all steps."""
        self.load_page()
        self.scroll_page()
        page_text = self.extract_page_text()
        self.parse_listings(page_text)
        df = self.create_dataframe()
        filtered_df = self.filter_dataframe(df)
        self.close()
        return filtered_df


# Manually parsed listings data
listings_data = [
    {"Address": "5358 Carolina Hwy, Denmark, SC 29042", "Price": 220000, "Beds": 7, "Baths": 9, "Sqft": 4187},
    {"Address": "302 West Rd, Greer, SC 29650", "Price": 213000, "Beds": 3, "Baths": 2, "Sqft": 1484},
    {"Address": "4293 Brandy Creek Ct #91, Clover, SC 29710", "Price": 199900, "Beds": 4, "Baths": 4, "Sqft": 3272},
    {"Address": "121 Spring Water Dr, Lexington, SC 29073", "Price": 209900, "Beds": 3, "Baths": 3, "Sqft": 1936},
    {"Address": "7 Stone Meadow Rd, Greenville, SC 29615", "Price": 215000, "Beds": 2, "Baths": 2, "Sqft": 1457},
    {"Address": "600 Norfolk St, Florence, SC 29506", "Price": 190000, "Beds": 3, "Baths": 2, "Sqft": 1409},
    {"Address": "587 Pine St, Warrenville, SC 29851", "Price": 240000, "Beds": 3, "Baths": 2, "Sqft": 1551},
    {"Address": "217 Pleasant Dr, Greer, SC 29651", "Price": 225000, "Beds": 3, "Baths": 2, "Sqft": 1266},
    {"Address": "718 Kingsbridge Rd, Columbia, SC 29210", "Price": 249000, "Beds": 4, "Baths": 3, "Sqft": 2424},
    {"Address": "204 Forest Ave, Anderson, SC 29625", "Price": 173000, "Beds": 3, "Baths": 3, "Sqft": 2017},
    {"Address": "1114 Lakeview Blvd, Hartsville, SC 29550", "Price": 215000, "Beds": 3, "Baths": 2, "Sqft": 1600},
    {"Address": "2983 Highway 418, Fountain Inn, SC 29644", "Price": 114900, "Beds": 3, "Baths": 3, "Sqft": 1750},
    {"Address": "476 Live Oak Church Rd., Loris, SC 29569", "Price": 235000, "Beds": 3, "Baths": 2, "Sqft": 1438},
    {"Address": "2410 High St, Columbia, SC 29203", "Price": 129000, "Beds": 3, "Baths": 1, "Sqft": 1302},
    {"Address": "190 Boys Home Rd, Pauline, SC 29374", "Price": 239900, "Beds": 4, "Baths": 3, "Sqft": 2459},
    {"Address": "160 Fairway Grn, Anderson, SC 29621", "Price": 179900, "Beds": 4, "Baths": 2, "Sqft": 1935},
    {"Address": "37 Vanderbilt Dr, Aiken, SC 29803", "Price": 235000, "Beds": 3, "Baths": 2, "Sqft": 1550},
    {"Address": "1368 E Old Marion Hwy, Florence, SC 29506", "Price": 199500, "Beds": 3, "Baths": 2, "Sqft": 1619},
    {"Address": "425 Brantley Dr, Hartsville, SC 29550", "Price": 240000, "Beds": 3, "Baths": 2, "Sqft": 2061},
    {"Address": "613 Cantey Pkwy, Camden, SC 29020", "Price": 185000, "Beds": 3, "Baths": 2, "Sqft": 1320},
    {"Address": "505 Forestbrook Dr., Myrtle Beach, SC 29579", "Price": 239500, "Beds": 4, "Baths": 2, "Sqft": 1569},
    {"Address": "102 Huntingridge Pl, Summerville, SC 29486", "Price": 185000, "Beds": 4, "Baths": 3, "Sqft": 1834},
    {"Address": "76 Proud Hope Ln, Due West, SC 29639", "Price": 75000, "Beds": 2, "Baths": 2, "Sqft": 1534},
    {"Address": "205 Woodlands W, Columbia, SC 29229", "Price": 225000, "Beds": 3, "Baths": 3, "Sqft": 2007},
    {"Address": "2730 Cultra Rd., Conway, SC 29526", "Price": 147900, "Beds": 2, "Baths": 1, "Sqft": 2548},
    {"Address": "924 Bridge St, Saint Matthews, SC 29135", "Price": 95000, "Beds": 3, "Baths": 2, "Sqft": 1615},
    {"Address": "300 E Myles Ln, Spartanburg, SC 29303", "Price": 220000, "Beds": 3, "Baths": 2, "Sqft": 1251},
    {"Address": "1600 Bolt Dr, Anderson, SC 29621", "Price": 225000, "Beds": 3, "Baths": 2, "Sqft": 1500},
    {"Address": "117 Dover Rd, Spartanburg, SC 29301", "Price": 250000, "Beds": 3, "Baths": 3, "Sqft": 2010},
    {"Address": "117 Whitehurst Way, Columbia, SC 29229", "Price": 185000, "Beds": 3, "Baths": 2, "Sqft": 1623},
    {"Address": "2109 Apple Valley Rd, Columbia, SC 29210", "Price": 195000, "Beds": 4, "Baths": 2, "Sqft": 1734},
    {"Address": "2816 Pisgah Rd, Florence, SC 29501", "Price": 225000, "Beds": 2, "Baths": 2, "Sqft": 1520},
    {"Address": "206 Gibert St, Union, SC 29379", "Price": 250000, "Beds": 4, "Baths": 3, "Sqft": 3583},
    {"Address": "93 Orchard Dr, Inman, SC 29349", "Price": 239900, "Beds": 3, "Baths": 2, "Sqft": 1835},
    {"Address": "1419 Hobart Dr, Florence, SC 29501", "Price": 235000, "Beds": 3, "Baths": 2, "Sqft": 1704},
    {"Address": "27031 Pocotaligo Rd, Yemassee, SC 29945", "Price": 240000, "Beds": 3, "Baths": 2, "Sqft": 1962},
    {"Address": "3205 W Bobo Newsom Hwy, Hartsville, SC 29550", "Price": 209900, "Beds": 3, "Baths": 2, "Sqft": 1580},
    {"Address": "117 Wrightson Ave, Spartanburg, SC 29306", "Price": 210000, "Beds": 3, "Baths": 2, "Sqft": 1646},
    {"Address": "8261 Truman Ave, Aiken, SC 29803", "Price": 185000, "Beds": 3, "Baths": 2, "Sqft": 1545},
    {"Address": "131 Whixley Ln, Columbia, SC 29223", "Price": 209900, "Beds": 3, "Baths": 2, "Sqft": 1266},
    {"Address": "320 Woodview Ave, Spartanburg, SC 29306", "Price": 150000, "Beds": 4, "Baths": 3, "Sqft": 2300}
]

# Create a DataFrame from the manually parsed data
df_manual = pd.DataFrame(listings_data)

# Combine with the scraped data
if __name__ == "__main__":
    zillow_url = 'https://www.zillow.com/sc/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22west%22%3A-85.244241453125%2C%22east%22%3A-76.608987546875%2C%22south%22%3A31.040569203933313%2C%22north%22%3A36.16170585540743%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A51%2C%22regionType%22%3A2%7D%5D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22price%22%3A%7B%22max%22%3A250000%7D%2C%22mp%22%3A%7B%22max%22%3A1174%7D%2C%22beds%22%3A%7B%22min%22%3A2%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22sqft%22%3A%7B%22min%22%3A1250%7D%2C%22hoa%22%3A%7B%22max%22%3A50%7D%2C%22ac%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A7%2C%22usersSearchTerm%22%3A%22SC%22%7D'

    scraper = ZillowScraper(zillow_url)
    scraped_listings = scraper.scrape()

    # Combine manual and scraped data
    combined_df = pd.concat([df_manual, scraped_listings], ignore_index=True)

    # Display the combined DataFrame
    print(combined_df)
