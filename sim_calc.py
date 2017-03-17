# -*- coding: utf-8 -*-

from gensim.models import word2vec
import jieba
import logging
import sys

def get_sentence_vector(sentence,model,stopwordset):
	word_vector_list = []
	
	words = jieba.cut(sentence, cut_all=False)
	
	for word in words:
		if word not in stopwordset and word.strip()!='':
			word_vector_list.append(model[word])
	
	result_vector = [0] * 250
	
	for i in range(250):
		for vector in word_vector_list:
			result_vector[i] += vector[i]
		if(len(word_vector_list)!=0):
			result_vector[i] /= len(word_vector_list)
	
	return result_vector	

def calc_sim(vector1,vector2):
	dot_product = 0.0  
	normA = 0.0  
	normB = 0.0  
	for a,b in zip(vector1,vector2):  
		dot_product += a*b  
		normA += a**2  
		normB += b**2  
	if normA == 0.0 or normB==0.0:  
		return None  
	else:  
		return dot_product / ((normA*normB)**0.5)  

def main():

	logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
	
	#if(len(sys.argv)!=3):
	#	logging.info("usage: python " + sys.argv[0] + " sentence1 sentence2")
	#	exit()

	# load stopwords set
	stopwordset = set()
	with open('stopwords.txt','r',encoding='utf-8') as sw:
		for line in sw:
			stopwordset.add(line.strip('\n'))
			
	model = word2vec.Word2Vec.load_word2vec_format("med250.model.bin", binary=True)
	
	while True:
		sent1 = input("请输入第一句话：")
		sent2 = input("请输入第二句话：")	
	
	#sent1 = sys.argv[1]
	#sent2 = sys.argv[2]
		try:	
			vector1 = get_sentence_vector(sent1,model,stopwordset)
			vector2 = get_sentence_vector(sent2,model,stopwordset)

			similarity = calc_sim(vector1,vector2)
	
			print("相似度：" + str(similarity))
		except Exception as e:
			print(e)

if __name__ == "__main__":
	main()
