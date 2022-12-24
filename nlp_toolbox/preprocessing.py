""" 
Funções que podem ser utilizadas no tratamento de texto e possível extração de insights 

"""
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from collections import Counter

from nltk import tokenize
import nltk, re, string, collections
from nltk.util import ngrams # function for making ngrams
from nltk.stem import RSLPStemmer # Steeming


def lower_case(data):
    
    # Apply Lower Case
    # Date input: as list of comments Ex: [CoMMent1,COmment2..] - > Date output: as array of comments Ex: [[comment1,comment2..]]
    
    import numpy as np
    
    data = np.char.lower(data)
    
    return data


def remove_punctuation(data):
    
    # Remove punctuation and symbols
    # Date input: array of comments [[c?omment1!],[comm?*ent2]...] - > Date output: as array of comments Ex: [[comment1,comment2..]]

    import numpy as np
    
    symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"
    for i in range(len(symbols)):
        data = np.char.replace(data, symbols[i], ' ')
        data = np.char.replace(data, "  ", " ")
    data = np.char.replace(data, ',', '')
    return data


def remove_stopword(data,
                    list_of_sentences = False,
                    include_stop = [],
                    keep_stop = []):
    
    # include_stop: list of  stopwords that you want to include
    # keep_stop : list of stop that you want to keep 
    # list_of_sentences = True -> Date input: list of sentences [[comment1],[comment2]...] --> Date output: list of words from sentence [[word1,word2...],[word1,word2...]...]
    # list_of_sentences = False -> Date input: list of sentences [[comment1],[comment2]...] --> Date output: list of all words without stopwords " [word1 word2 word3 word4] "
    
    import nltk
    nltk.download('stopwords');
    stopwords = nltk.corpus.stopwords.words('portuguese');
    
    newstopwords = ['pro','pra','sim','possa','q','ja','ta','n','aff','ta','aaah w','ter','não','nao','s','vc','n°','da','ñ','r','tá','esyer','vivo']
    newstopwords += include_stop
    appendwords = keep_stop

    stop = list(nltk.corpus.stopwords.words('portuguese'))
    stop.extend(newstopwords)
    stop.append(appendwords)
    
        
    #print(stop)

    data_wo_stop = []
    
    # Alguns tratamentos dentro da lista - pipeline

    for i in data:

        lista = [palavra for palavra in i.split(" ") if palavra not in stop] # remove stopword
        
        lista = [palavra for palavra in lista if not palavra.isdigit() ] # remove números 
        
        lista = [palavra for palavra in lista if palavra != ''] # remove espaços vazios
        
        if len(lista) != 0: # Se não for uma lista vazia ( ou seja quando o usuário coloca apenas 'não')
                        
            data_wo_stop.append(lista) # cria nova lista que esta tratada
            
        else: 
            
            pass
        
    data = data_wo_stop
    
    text_list = []
        
    if list_of_sentences == False:
        
        for i in data:

            text_list += i

        return text_list

    else:       
                   
        return data


    
    
""" Necessário correção  !!!! """
'''
def stemmer_pt(data):
    
    """ Necessário correção  !!!! """
    

    """ Busca encontrar apenas raiz da palavra, pode cortar até demais."""
    

    import nltk
    nltk.download('rslp')
    
    data = [[stemmer.stem(palavra) for palavra in sublist]for sublist in data]
    
    return data'''
'''
def words_pipeline(data):
    
    print(data[0:10])
    lista = lower_case(data)
    print(lista[0:10])
    print("Lower Case 1 :----------------------")
    lista2 = remove_punctuation(lista)
    print(lista2[0:10])
    print("Punctuation 2 :----------------------")
    lista3 = remove_stopword(lista2)
    print(lista3[0:10])
    print("Stopword 3 :----------------------")
    
    return data
'''


def generate_ngrams(text, n_gram=1,stop=True,newstopwords=[],appendwords=[]):
    
    '''
    Simple n-gram generator.
    '''
    newstopwords=newstopwords
    appendwords = appendwords
    
    if stop:
        
        stop = list(nltk.corpus.stopwords.words('portuguese'))
        stop.extend(newstopwords)
        stop.append(appendwords)
        
        
    else:
        
        pass
              
    token = [token for token in str(text).lower().split(" ") if token != "" if token not in stop]
    
    z = zip(*[token[i:] for i in range(n_gram)])
    ngrams = [" ".join(ngram) for ngram in z]
    
    return ngrams


def plot_word(text, n_grams=2, head=30,**kwargs):
    
    """Input = text and return dataframe""" 
    
    import plotly.express as px
    import pandas as pd
    
    # Input: Text data pré-processed  -> Output = Barplot with frequencies sorted
    
    df = pd.DataFrame(collections.Counter(generate_ngrams(text, n_gram=n_grams)).most_common(head),columns =['Palavra', 'Frequencia'])    
    
    #Plotting
    
    fig = px.bar(df.sort_values('Frequencia', ascending=False), x='Palavra', y='Frequencia',**kwargs)
    return fig.show()


""" 
Function to receive an text, use n-grams (2) and return an dataframe ready to networks use, 
with sentence,'target','source' and weight that's the frequency of this n-gram in text 
"""

def text_network(text,n_gram=2):
    
    import pandas as pd
    import collections
    
    two_gram = collections.Counter(pe.generate_ngrams(text, n_gram=2)) # Return a "Counter with dict"
    
    df = pd.DataFrame(two_gram.items())
    df[['target','source']] = df[0].str.split(' ',expand=True)
    df.rename(columns={0:'n_gram',1:'weight'},inplace=True)
    
    return df