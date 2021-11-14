import requests
from bs4 import BeautifulSoup
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
from selenium.webdriver.common.keys import Keys

class WebScrape:
    def __init__(self):
        self.league_dic = {}
        self._get_league_match_urls()

    def init_selenium(self):
        self.chrome_options = Options()
        #self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument("--mute-audio")
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.chrome_options.add_argument("--autoplay-policy=no-user-gesture-required")
        self.driver = webdriver.Chrome(r"C:\Users\itsuk\Documents\Projects\StreamerPI\ChromeDriver\chromedriver",options=self.chrome_options)

    def _get_league_match_urls(self):

        # Get main soccer stream page
        main_soccer_stream_url = "https://buffersports.com/football-games"
        
        # Find match and link of it
        main_soccer_page = requests.get(main_soccer_stream_url)
        main_soccer_content = BeautifulSoup(main_soccer_page.content, "html.parser").find_all("li", {"class" : "country-sales-content list-group-item"})
        
        for league in main_soccer_content:
            
            # Extract name of league
            league_name = league.find(class_ = "ml-3 mt-3 font-weight-bold").text.strip()
            if league_name:
                # Create entry for dictionary
                self.league_dic[league_name] = {}
                
                # Extract matches in league
                matches = league.find_all(class_ = "row mt-3")
                for match in matches:
                    # Extract match description, match time and match link
                    match_description = match.find(text=re.compile(r'\w+ vs \w+'))
                    match_time_utc = match.find(text=re.compile(r'[0-9]{2}:[0-9]{2} [APM]{2}')).strip()
                    match_link = match.find(class_ = "text-dark col text-center").find("a").attrs["href"]

                    # Record them in dictionary
                    self.league_dic[league_name].update({match_description : {"Time" : match_time_utc, "match_link": match_link, "stream_link": [], "m3u8" : []}})

    def get_all_match_urls(self):
        for league_name in self.league_dic:
            for match_description in self.league_dic[league_name]:
                self.get_matches_urls(league_name, match_description)

    def get_matches_urls(self, league, match):
        
        # Go to match's link
        match_link = self.league_dic[league][match]["match_link"]
        match_page = requests.get(match_link)
        match_content_url = BeautifulSoup(match_page.content, "html.parser").find('iframe').attrs['src']
        match_page = requests.get(match_content_url)

        # Get all link that you can stream from and save it in self.league_dic
        match_links = BeautifulSoup(match_page.content, "html.parser").find_all("a")[1:]
        for link in match_links:

            target_attribute = ""
            try:
                target_attribute = link.attrs["target"]
            except:
                target_attribute = ""
            finally:
                stream_link = (target_attribute == "_blank")
            
            if stream_link:
                match_link =  link.attrs["href"]
                self.league_dic[league][match]["stream_link"].append(match_link)

    def video_finder(self, url):
        
        m3u8_urls = []
        #self.driver = webdriver.Chrome(r"C:\Users\itsuk\Documents\Projects\StreamerPI\ChromeDriver\chromedriver",options=self.chrome_options)
        self.driver.set_page_load_timeout(15)

        try:
            self.driver.get(url)
        except:
            print("send escape")
            self.driver.find_element_by_tag_name("body").send_keys(Keys.ESCAPE)

        try:
            self.driver.wait_for_request(".m3u8", 15)
            print("m3u8 url found")
            for request in self.driver.requests:
                if request.response and ("m3u8" in request.url):
                    if request.url not in m3u8_urls:
                        m3u8_urls.append(request.url)

        except:
            print("no m3u8 url")
            m3u8_urls = []

        return (m3u8_urls)


if __name__ == "__main__":
    obj = WebScrape()
    obj.get_all_match_urls()

    print (obj.league_dic)


