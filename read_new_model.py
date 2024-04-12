import gensim
import json
import string
import re
import nltk
import numpy as np
from decimal import Decimal

models = gensim.models.KeyedVectors.load("./newmodell.bin")
#print(models.get_vector("акции"))

with open('./tickers.json', 'r') as infile:
    infile_dict = json.load(infile)

for_all_tickers = {}
for ticker in infile_dict:
    global_text = ''
    global_dict = {}
    for item in infile_dict[ticker]:
        text = item['content']['text']
        date = item['inserted'].split('T')[0]
        text = text.lower()
        spec_chars = string.punctuation + '\n\xa0«»\t—…' 

        text = re.sub(r'http\S+', '', text)
        text = "".join([ch for ch in text if ch not in spec_chars])

        emoj = re.compile("["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                u"\U00002500-\U00002BEF"  # chinese char
                u"\U00002702-\U000027B0"
                u"\U000024C2-\U0001F251"
                u"\U0001f926-\U0001f937"
                u"\U00010000-\U0010ffff"
                u"\u2640-\u2642" 
                u"\u2600-\u2B55"
                u"\u200d"
                u"\u23cf"
                u"\u23e9"
                u"\u231a"
                u"\ufe0f"  # dingbats
                u"\u3030"
                            "]+", re.UNICODE)
        text = re.sub(emoj, '', text)
        text = "".join([ch for ch in text if ch not in string.digits])
        text_tokens = nltk.word_tokenize(text)
        r = re.compile("[а-яА-Я]+")
        text_tokens = [w for w in filter(r.match, text_tokens)]
        russian_stopwords = nltk.corpus.stopwords.words("russian")
        russian_stopwords.extend(['это'])

        for s in russian_stopwords:
            text_tokens.remove(s) if s in text_tokens else True
        
        if date not in global_dict:
            global_dict[date] = []
        result = {'likes': item['likesCount'], 'text': text_tokens}
        global_dict[date].append(result)
    
    for_all_tickers[ticker] = global_dict

#print(global_dict)
with open('tokens_for_date_text.json', 'w', encoding='utf8') as outfile:
    json.dump(for_all_tickers, outfile, ensure_ascii=False)
    #global_text+=' '+text

result_vectors = {}
for ticker in for_all_tickers:
    result_vectors[ticker] = {}
    for day in for_all_tickers[ticker]:
        
        temp_vector_with_likes = []
        all_likes_for_day = 0
        for text in for_all_tickers[ticker][day]:
            if text['text'] != []:
            #    text['text'] = [x if x in list(models.key_to_index) else '<PAD>' for x in text['text']]
            #print(text)
            #print([models.vectors[models.key_to_index[token]] for token in text['text'] if token in list(models.key_to_index)])
                #try:
                response_vector = np.mean([models.vectors[models.key_to_index[token]] if token in list(models.key_to_index) else np.zeros(300) for token in text['text'] ], axis=0) 
                #response_vector = np.mean([models.vectors[models.key_to_index[token]] if token in list(models.key_to_index) else '<PAD>' for token in text['text']], axis=0)  
                all_likes_for_day += text['likes']
                #smisl = np.linalg.norm(response_vector)
                new_resp_vect = [x*text['likes'] for x in response_vector]
                temp_vector_with_likes.append(new_resp_vect)
                #except:
                #    print(text['text'])
                #print(len(response_vector))
        if all_likes_for_day==0:
            result_vectors[ticker][day] = [0]*300
        else:
            new_vect = [0]*300
            for s in temp_vector_with_likes:
                for i in range(0,300):
                    new_vect[i] += s[i] 
            #print(new_vect)
            #total = 0
            #for i in new_vect:
            #    total+=i
            #print(total/all_likes_for_day)
            result_vect = [0]*300
            for i in range(0,300):
                result_vect[i]='%.3E' % Decimal(new_vect[i]/all_likes_for_day)
            #print(result_vect)
            result_vect=np.array(result_vect,dtype=float)
            result_vectors[ticker][day] = result_vect.tolist()
        #print(result_vect)
            #day_likes = 0
            #itog = 0
            #for vector in temp_vector_with_likes:
                #itog+=vector[0]
            #    day_likes += vector[0]
            
            #print(itog/day_likes)
            #print(temp_vector_with_likes)
            #print('\n#######################################################################\n')
                #if smisl < 2.13:
                #   print(text)
with open('final_res_vectors.json', 'w') as outfile:
    json.dump(result_vectors, outfile)


    
#while True:
#    if global_text.find('  ') != -1:
#        global_text = global_text.replace('  ', ' ')
#    else:
#        break

#print(global_text)
#print(models.get_vector("акция"))
#print(models)