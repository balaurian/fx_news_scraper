from urllib.request import Request, urlopen
import datetime

from bs4 import BeautifulSoup as bs
import pandas as pd

class fx_news_scraper():
    def __init__(self):
        # 
        # The scraped csv file is written on disk after the whole scraping is done. 
        # This is a problem when the connection drops and all scraping is lost 
        # Therefore you need to set how many pages you would need to scrap. 
        # Keep this number low while testing/debugging
        #
        self.number_of_pages = 3
        self.news_list = []
        self.target_url = 'https://www.investing.com/news/forex-news/'
        self.output_csv = 'app/data/fx-news-archive.csv'


    def scraper(self):
        for page_no in range(1, self.number_of_pages) :
            url = self.target_url + str(page_no)

            req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})
            
            webpage = urlopen(req).read()

            soup = bs(webpage, "html.parser")
            
            div_navigation = soup.find('div', id = 'paginationWrap')

            navigation = div_navigation.find('div', class_ = 'sideDiv inlineblock text_align_lang_base_2').text
            
            if len(navigation) != 1:
                
                div = soup.find('div', class_= 'largeTitle')
                
                now = datetime.datetime.now()
                date = datetime.datetime

                for news_div in div.find_all('div', class_= 'textDiv'):
                    news_title_a = news_div.find('a', class_ = 'title')
                    news_body    = news_div.find('p')
                    news_date    = news_div.find('span', class_ = 'date')
                    news_href    = news_title_a.get('href')

                    if news_date is not None:
                        news_date = news_date.text
                        
                        if 'hours' in news_date:
                            news_date = now.strftime("\xa0-\xa0%b %d, %Y")
                        if 'hour' in news_date:
                            news_date = now.strftime("\xa0-\xa0%b %d, %Y")
                        if 'minutes' in news_date:
                            news_date = now.strftime("\xa0-\xa0%b %d, %Y")

                        if '-' in news_date:
                            date_news_date = date.strptime(news_date, "\xa0-\xa0%b %d, %Y")
                            
                            self.news_list.append([page_no, date_news_date, news_title_a.text , news_body.text ])
                            
                        news_dataset = pd.DataFrame(self.news_list, columns = ['page', 'date','title','body'] )
                    
                page_no += 1
                    
            else:
                continue

        news_dataset.to_csv(self.output_csv)
        print ('scraping completed')
        print ('output --> app/data/fx-news-archive.csv')