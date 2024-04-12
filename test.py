import json
import string
import re
import nltk

with open('./tickers.json', 'r') as infile:
    infile_dict = json.load(infile)

global_text = ' '
for ticker in infile_dict:
    temp_text = ''
    for item in infile_dict[ticker]:
        text = item['content']['text']
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
        temp_text+=' '+text

    global_text+=temp_text
while True:
    if global_text.find('  ') != -1:
        global_text = global_text.replace('  ', ' ')
    else:
        break

text = global_text
    #nltk.download('punkt')
text_tokens = nltk.word_tokenize(text)
r = re.compile("[а-яА-Я]+")
text_tokens = [w for w in filter(r.match, text_tokens)]

text = nltk.Text(text_tokens)

fdist = nltk.probability.FreqDist(text)
russian_stopwords = nltk.corpus.stopwords.words("russian")

russian_stopwords.extend(['это'])

for s in russian_stopwords:
    fdist.pop(s) if s in fdist.keys() else True

import json
vacabular = {}
vacabular['vacabular'] = dict(fdist.items())
with open('vacabular.json', 'w', encoding='utf-8') as outfile:
    json.dump(vacabular, outfile, ensure_ascii=False)
print(nltk.corpus.stopwords.words("russian"))
print(fdist.items())
print(len(fdist.keys()))
#russian_stopwords = nltk.corpus.stopwords.words("russian")
#without_stopwords = list(set(text_tokens)-set(russian_stopwords))


#print(fdist.most_common(15))

##############


#without_stopwords_and_english = [w for w in filter(r.match, without_stopwords)]
#text2 = nltk.Text(without_stopwords_and_english)
#fdist2 = nltk.probability.FreqDist(text2)
##############


#without_stopwords_and_english2 = []
#for i in without_stopwords:
#    try:
#        i.encode('ascii')
#    except:
#        without_stopwords_and_english2.append(i)

#print(len(without_stopwords_and_english), len(without_stopwords_and_english2))
#print(list(fdist.keys()))

#print(text)
#print(text.encode('ascii'))
#print(infile_dict['VKCO'][0]['content']['text'].replace(',',''))
#for s in infile_dict:
#    print(len(infile_dict[s]))
