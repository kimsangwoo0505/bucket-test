from flask import Flask, render_template, request, jsonify
application = app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.ing0uyy.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta#dbprac.py에서 가져옴

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']#백엔드에서 받아 sample_receive라는변수에 넣음

    bucket_list = list(db.bucket.find({}, {'_id': False}))
    count = len(bucket_list) + 1
    
    doc = {
        'num':count,  #버킷 등록 시, db에서 특정 버킷을 찾기 위해 'num' 이라는 고유 값 부여
        'bucket' :bucket_receive,
        'done' : 0   #'done' key값을 추가 해 각 버킷의 완료 상태 구분(0 = 미완료, 1 = 완료)
    }
    db.bucket.insert_one(doc)#doc형태로 서버에 저장함
    return jsonify({'msg': '저장 완료!'})##메세지를 프론트엔드에 보냄(?)


############## API 만드는 곳#########################
@app.route("/moviedele", methods=["POST"])
def movie_del():
    con_receive = request.form['con_give']   
    print(con_receive)  
    db.bucket.update_one({'num': int(con_receive)},{'$set':{'done':1}})   
   # db.bucket.delete_one({'num': 7})
    return jsonify({'msg':'완료'})
#####################################################


@app.route("/bucket", methods=["GET"])#프론트엔드에서 받아옴(?)
def bucket_get():
    all_buckets = list(db.bucket.find({},{'_id':False}))
    return jsonify({'result': all_buckets})#서버에서'result': all_buckets을받아 프론트엔드로 보냄

if __name__ == '__main__':
    app.run()