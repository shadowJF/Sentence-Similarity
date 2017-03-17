from flask import Flask
from flask import request
from flask import jsonify
from flask import abort
from gensim.models import word2vec
import jieba
from sim_calc import *

app = Flask(__name__)

stopwordset = set()
with open('stopwords.txt','r',encoding='utf-8') as sw:
    for line in sw:
        stopwordset.add(line.strip('\n'))

model = word2vec.Word2Vec.load_word2vec_format("med250.model.bin", binary=True)

@app.route('/')
def index():
    print(lists)
    return "Hello, World!"


@app.route('/robot/simcalc', methods=['POST'])
def get_most_sim_sentences():
    if not request.json:
        return jsonify({'code':0,'text':"请保证body数据为json格式"}) , 200
    if not 'sentence' in request.json:
        return jsonify({'code':0,'text':"sentence为空"}) , 200
    if not 'complist' in request.json:
        return jsonify({'code':0,'text':"complist为空"}) , 200

    sent = request.json['sentence']

    try:
        sent_vector = get_sentence_vector(sent,model,stopwordset)
    except Exception as e:
        return jsonify({"code":0,'text':"问题转向量模型出错："+str(e)}) , 200

    candidate_list = request.json['complist']
    max_sim_list = []

    number = request.json.get('number',5)
    sim_threshold = request.json.get('threshold',0.8)

    for candidate in candidate_list:
        try:
            candidate_origin = candidate['origin']
            candidate_keywords = candidate['keywords']
            vec = get_sentence_vector(candidate_keywords,model,stopwordset)
            sim = calc_sim(sent_vector,vec)
            if sim > sim_threshold:
                candi_dict = {"sentence":candidate_origin,"similarity":sim}
                if len(max_sim_list) < number:
                    max_sim_list.append(candi_dict) 
                else:           
                    min_sim_candi = min(max_sim_list,key=lambda x: x['similarity'])
                    if sim > min_sim_candi['similarity']:
                        index = max_sim_list.index(min_sim_candi)
                        max_sim_list[index] = {"sentence":candidate_origin,"similarity":sim}
        except Exception as e:
            print(e)

    max_sim_list.sort(key=lambda x: x['similarity'],reverse=True)
    return jsonify({"code":1,'data':max_sim_list}) ,200        

if __name__ == '__main__':
    app.run(host='0.0.0.0')
