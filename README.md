# Sentence-Similarity

计算短句之间的相似度

基本思想为：利用jieba分词对句子分词，然后利用word2vec获得所有词语的词向量，最后将该句子中所有词的词向量相加取平均即得到该句子的句向量，最后利用余弦相似度算法计算句子间的相似度

* wiki_to_txt.py是将wiki xml语料转为文本的代码
* segment.py是对文本进行分词的代码
* train.py是对语料进行训练得到word2vec模型的代码
* sim_calc.py是计算两个句子间余弦相似度的代码

具体参考：我的个人博客[Chat Robot](http://shadowjf.github.io/2017/02/08/Chat-Robot.html)
