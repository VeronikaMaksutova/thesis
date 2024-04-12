from tpulse import TinkoffPulse 
import threading
import json
import requests
import io
pulse = TinkoffPulse() 
#ticker = 'AAPL'

tickers = ["VKCO", "LKOH", "FLOT", "GAZP", "ROSN", "SBER", "SNGSP", "MGNT", "TRNFP", "YNDX"]
#VTBR AMD INTC TSLA, APPL, GAZP, FB, AMZN, NVDA, PFE 
def loader(ticker):
    cursor_value = 9999999999 
    target_date = "2023-09-01" 
    for ticker in tickers: 
        continue_loading = True 
        for num in range(1, 300+1): 
            if not continue_loading: 
                break   
            ticker_posts = pulse.get_posts_by_ticker(ticker, cursor_value) 
            cursor_value = ticker_posts["nextCursor"] 
            if len(ticker_posts.get("items")) == 0: 
                break 
            for item in ticker_posts['items']: 
                if 'content' in item and 'text' in item['content']: 
                    text_value = item['content']['text'].replace('\n', ' ') 
                    date = item['inserted'].replace('T', ' ').split('.')[0] 

                    if date < target_date: 
                        continue_loading = False   
                        break   

                    #print(text_value) 
                    #loadString(text_value, ticker, date, predicted_class) 
                    #insert("tcs_pulse_posts", parsed) 
        #    sleep(choice(range(2, 4)))

   
from datetime import date, timedelta
import time

if __name__=="__main__":
    headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'accept': '*/*',
    'content-type': 'application/x-www-form-urlencoded',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    tickers_dict={}
    last_date = date(2024, 3, 1)
    cursor = 9999999999
    for ticker in tickers:
        temp_ticker_list = []
        while True:
            try:
                ticker_data_response=requests.get(f'https://www.tinkoff.ru/api/invest-gw/social/v1/post/instrument/{ticker}?cursor={cursor}', headers=headers)
                ticker_data = ticker_data_response.json()
            except:
                print('SLEEP')
                time.sleep(65)
                #cursor = 9999999999
                #break
            #ticker_data = ticker_posts = pulse.get_posts_by_ticker(ticker, cursor) 
            #print(ticker_data)
            last_page_date = ticker_data['payload']['items'][-1]['inserted']
            #last_page_date = ticker_data['items'][-1]['inserted']
            splitted_last_page = last_page_date.split('T')
            last_page_date = date(int(splitted_last_page[0].split('-')[0]), int(splitted_last_page[0].split('-')[1]),int(splitted_last_page[0].split('-')[2]))
            #print(last_date - last_page_date > timedelta(0))
            #print(last_date)
            #print(last_page_date)
            if last_date - last_page_date > timedelta(0):
                cursor = 9999999999
                print('BBBBBBB')
                break
            else:
                #print('AAAAAA'+ticker)
                temp_ticker_list += ticker_data['payload']['items']
                cursor = ticker_data['payload']['nextCursor']
                #temp_ticker_list += ticker_data['items']
                #cursor = ticker_data['nextCursor']
        tickers_dict[ticker] = temp_ticker_list
    with open("./tickers2.json", 'w', encoding='utf8') as outfile:
        json.dump(tickers_dict, outfile, ensure_ascii=False)
            #break
                #if 'content' in item and 'text' in item['content']: 
                #    text_value = item['content']['text'].replace('\n', ' ') 
                #    last_date = item['inserted'].replace('T', ' ').split('.')[0] 
                #    if last_date < last_date: 
                #        continue_loading = False   
                #        break   
        #print(ticker_data)
        #with open("./temp.json", 'w', encoding='utf8') as tempfile:
            #json.dump(ticker_data,outfile, ensure_ascii=False)
        #    tempfile.write(ticker_data)
        #with open("./temp.json", 'r', encoding='utf8') as tempfile:
        #    tempdict = json.load(tempfile)
        #with open("./temp.json", 'r') as tempfile:
            
        #print(ticker_data)
        #print(ticker_data.decode('utf-8'))
        #ticker_data = ticker_data.replace('\\u', '')
        #tickers_dict[ticker]=tempdict
    #with open("./tickers.json", 'w', encoding='utf8') as outfile:
    #    json.dump(tickers_dict, outfile, ensure_ascii=False)
    #with io.open("./tickers.json", 'w', encoding='utf-8') as fh:
    #    fh.write(json.dumps(decode_dict(reg_dict), ensure_ascii=False))
    #    except:
    #        pass
    #print(len(ticker_posts['items'])) 