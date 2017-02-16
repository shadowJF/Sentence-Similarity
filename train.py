# -*- coding: utf-8 -*-

from gensim.models import word2vec
import logging

def main():

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    
    sentences = word2vec.Text8Corpus("wiki_seg.txt")
    model = word2vec.Word2Vec(sentences, size=250)
    model.save_word2vec_format(u"med250.model.bin", binary=True)

    # how to load a model ?
    # model = word2vec.Word2Vec.load_word2vec_format("your_model.bin", binary=True)

if __name__ == "__main__":
    main()