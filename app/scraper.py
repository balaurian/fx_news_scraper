from bs4 import BeautifulSoup as bs
import pandas as pd
from urllib.request import Request, urlopen
from tqdm import tqdm

class fx_news_scraper():
    def __init__(self):
        self.number_of_pages = 29
        self.news_list = []
        self.target_url = 'https://www.investing.com/news/forex-news/'
        self.output_csv = 'app/data/fx-news-archive_test.csv'
        self.news_dataset = pd.DataFrame()

    def scraper(self):
        for page_no in tqdm(range(1, self.number_of_pages+1)):
            url = self.target_url + str(page_no)
            req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})
            
            webpage = urlopen(req).read()
            
            soup = bs(webpage, "html.parser")
            
            news_container_div = soup.find('div', class_= 'news-analysis-v2_articles-container__3fFL8 mdMax:px-3 mb-12')

            try:
                for news_div in news_container_div.find_all('div', class_= 'news-analysis-v2_content__z0iLP w-full text-xs sm:flex-1'):
                    news_title_a = news_div.find('a', class_ = 'text-inv-blue-500 hover:text-inv-blue-500 hover:underline focus:text-inv-blue-500 focus:underline whitespace-normal text-sm font-bold leading-5 !text-[#181C21] sm:text-base sm:leading-6 lg:text-lg lg:leading-7')
                    news_body    = news_div.find('p')
                    news_date    = news_div.find('time', class_ = 'mx-1 shrink-0 text-xs leading-4').get('datetime')
                    
                    news_href    = news_title_a.get('href')
                    
                    self.news_list.append([page_no, news_date, news_title_a.text , news_body.text, news_href])

                    
            except ValueError as vEr:
                print(vEr)

            
            self.news_dataset = pd.DataFrame(self.news_list, columns = ['page', 'date','title','body', 'url'] )
            self.news_dataset.to_csv(self.output_csv)
            
            page_no += 1

        print ('scraping completed')
        print (f'output --> {self.output_csv}')