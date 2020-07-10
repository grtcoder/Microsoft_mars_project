from flask import Flask,jsonify,request


app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
    if(request.method == 'GET'):
        data="I will return you whatever harshit want"
        return jsonify({'data':data})


@app.route('/processing/<int:num>',methods=['GET'])
def disp(num):
    return jsonify({'data':num**4})

if __name__ == '__main__':
    app.run(debug = True)

