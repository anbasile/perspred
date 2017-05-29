import pandas as pd
import xmltodict
import glob

def read_corpus():
    training_files = glob.glob('/home/ang/work/dataset/pan2015/*/*.xml',
                               recursive=True)
    temp = []
    for t in training_files:
        with open(t) as f:
            doc = xmltodict.parse(f.read())
        author = doc['author']['@id']
        lang = doc['author']['@lang']
        message = '\n'.join(doc['author']['document'])
        temp.append((author, lang, message))

    corpus_temp = pd.DataFrame(temp,
                               columns=['author', 'lang', 'text'])

    labels_files = [pd.read_csv(f,
                                sep='\:\:\:',
                                names=['author', 'gender', 'age',
                                       'ext', 'sta', 'agr', 'con', 'opn'],
                                engine='python',
                                usecols=[0, 1, 2, 3,
                                         4, 5, 6, 7]) for f in glob.glob('/home/ang/work/dataset/pan2015/*/*.txt',
                                                                      recursive=True)]
    labels_temp = pd.concat(labels_files)
    corpus = pd.merge(corpus_temp,
                      labels_temp,
                      on='author')
    return corpus
