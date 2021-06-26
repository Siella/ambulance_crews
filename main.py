#import Flask
from flask import Flask,render_template,request,redirect,url_for,flash
#create an instance of Flask
app = Flask(__name__)
@app.route('/',methods=['POST','GET'])
def home():
    if request.method=='POST':
        zone = request.form.get('zone')  # запрос к данным формы
        feature = request.form.get('feature')
        part=request.form.get('part')
        data=request.form.get('part')

        return  redirect(url_for('predict'))
    else:
        return render_template('home.html')

@app.route('/predict',methods=['POST','GET'])
def predict():
    return  render_template('predict.html')


if __name__ == '__main__':
    app.run(debug=True)