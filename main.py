import app.scraper
import app.tokenizer
import app.news_sort

def start():
    while True:
        usr_in = input('\n1. start scraping\n2. tokenization\n3. start sorting\n0. exit\n\ndo something\n')
        if usr_in == '1':
            print ('\n-->start scraping ...\n')
            news_scraper = app.scraper.fx_news_scraper()
            news_scraper.scraper()

        elif usr_in == '2':
            print ('\n-->start tokenizing ...\n')
            news_tokenizer = app.tokenizer.fx_news_tokenizer()
            news_tokenizer.start_tokenizing()
        
        elif usr_in == '3':
            print ('\n-->start sorting ...\n')
            app.news_sort.start_sorting()

        elif usr_in == '0':
            print ('\n-->exiting ...\n')
            break
        
        else:
            continue

if __name__ == '__main__':
    start()