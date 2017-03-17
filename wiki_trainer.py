# -*- coding: utf-8 -*-
import logging
import sys
import os
import jieba
from gensim.models import word2vec
from gensim.corpora import WikiCorpus

def wiki_to_text(wiki_data_path):
    logging.info("开始将维基语料转换为普通文本格式：")
    if os.path.exists("wiki_texts.txt"):
        return

    wiki_corpus = WikiCorpus(wiki_data_path, dictionary={})
    texts_num = 0

    with open("wiki_texts.txt",'w',encoding='utf-8') as output:
        for text in wiki_corpus.get_texts():
            output.write(b' '.join(text).decode('utf-8') + '\n')
            texts_num += 1
            if texts_num % 10000 == 0:
                logging.info("已处理 %d 篇文章" % texts_num)

def trad_to_simp():
    logging.info("开始将文本转换为简体中文：")
    if os.path.exists("wiki_texts_sim.txt"):
        return

    a = os.system('opencc -i wiki_texts.txt -o wiki_texts_sim.txt -c /usr/share/opencc/mix2zhs.ini')
    if a != 0:
        os._exit()

def segment():
    logging.info("开始对语料进行分词：")
    if os.path.exists("wiki_seg.txt"):
        return

    stopwordset = set()
    if os.path.exists("stopwords.txt"):
        logging.info("发现停用词词典，将会去除所有停用词！")
        with open('stopwords.txt','r',encoding='utf-8') as sw:
            for line in sw:
                stopwordset.add(line.strip('\n'))
    if os.path.exists("custom_dict.txt"):
        logging.info("发现自定义词库，加载自定义词库中")
        jieba.load_userdict("custom_dict.txt")

    output = open('wiki_seg.txt','w',encoding='utf-8')
    texts_num = 0

    with open('wiki_texts_sim.txt','r',encoding='utf-8') as content :
        for line in content:
            words = jieba.cut(line, cut_all=False)
            for word in words:
                if word not in stopwordset:
                    output.write(word +' ')
            texts_num += 1
            if texts_num % 10000 == 0:
                logging.info("已完成前 %d 行分词" % texts_num)
    output.close()

def train():
    logging.info("开始训练词向量模型: ")
    
    sentences = word2vec.Text8Corpus("wiki_seg.txt")
    model = word2vec.Word2Vec(sentences, size=250)
    model.save_word2vec_format(u"med250.model.bin", binary=True) 

def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    if len(sys.argv) != 2:
        print("Usage: python " + sys.argv[0] + " wiki_data_path")
        exit()

    wiki_to_text(sys.argv[1])
    trad_to_simp()
    segment()
    train()

if __name__ == "__main__":
    main()
