import gensim
import json
import numpy as np

model = gensim.models.KeyedVectors.load_word2vec_format("http://wikipedia2vec.s3.amazonaws.com/models/ru/2018-04-20/ruwiki_20180420_300d.txt.bz2")
print(model)
with open('vacabular.json', 'r', encoding='utf8') as outfile:
    vacabular_dict = json.load(outfile)

vacabular_list = list(vacabular_dict['vacabular'])
 
# Создайте новую модель с пустыми векторами 
new_model = gensim.models.KeyedVectors(vector_size=model.vector_size) 

# Сохраните только нужные векторы 
for word in vacabular_list: 
    if word in model: 
        new_model.add_vector(word, model[word]) 
    else:
        new_model.add_vector('<PAD>', np.zeros(300,dtype=float))
# Сохраните новую модель 
new_model.save("./newmodel.bin")