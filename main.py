#import Flask
import io
from datetime import timedelta
import matplotlib.dates as mdates
import pandas  as pd
import matplotlib.pyplot as plt
import base64
from flask_bootstrap import Bootstrap
import datetime as DT
global datas
from flask import Flask,render_template,request,redirect,url_for,flash
#create an instance of Flask
app = Flask(__name__)
def file(n):
    if n=='zone1':
        return 'total_Пстанция 1.csv'
    elif n=='zone2':
        return 'total_Пстанция 2.csv'
    elif n=='zone3':
        return 'total_Пстанция 3.csv'
    elif n=='zone4':
        return 'total_Пстанция 4.csv'
    elif n=='zone5':
        return 'total_Пстанция 5.csv'
    elif n=='zone6':
        return 'total_Пстанция 6.csv'
    elif n=='zone7':
        return 'total_Пстанция 7.csv'
    elif n=='zone8':
        return 'total_Пстанция 8.csv'
    elif n=='zone9':
        return 'total_Пстанция 9.csv'
bootstrap = Bootstrap(app)
@app.route('/',methods=['GET', 'POST'])
def home():
    if request.method=='POST':
        if request.form['submit_button'] == 'Пред. День':
            my_file = open("new.txt", 'r')
            my_string = my_file.readlines()
            my_file.close()
            for string in my_string:
                brigada = string.split(" ")[0]

                date = DT.datetime.strptime(string.split(" ")[1], '%Y-%m-%d').date()

                name = file(brigada)
                data = pd.read_csv('total_Пстанция 1.csv')
                column_name = 'total'
                data['date'] = pd.to_datetime(data['date'])
                data = data[['date', column_name]].groupby(data[['date', column_name]].date.dt.date).sum()
                for index, row in data.iterrows():
                    index = DT.datetime.strptime(str(index), '%Y-%m-%d').date()
                    print(index)
                    print(row)
                    if index == date:
                        print(data.index)
                        plt.gcf().autofmt_xdate()

                        newdf = data[(data.index > index - timedelta(days=7)) & (data.index < index + timedelta(days=7))]
                        fig = plt.figure(figsize=(10, 5), dpi=125)
                        myFmt = mdates.DateFormatter('%m-%d')
                        plt.gca().xaxis.set_major_formatter(myFmt)
                        plt.ylabel("Число вызывов ")
                        plt.xlabel("Дата")
                        plt.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
                        plt.xticks(rotation=45)
                        plt.plot(newdf, '.-', label='total')
                        plt.scatter(index, row, label='predict',c='#ff0000')
                        plt.legend()
                        plt.savefig('static/images/sdf.png')
                        first = newdf[:6]
                        second = newdf[7:]

                        total_f = first['total'].sum()
                        total_s = second['total'].sum()
                        if total_f > total_s:
                            pred = total_s / total_f
                            pred = f"Уменьшилось на {round((1 - pred) * 100, 2)}% "
                        else:
                            pred = total_f / total_s
                            pred = f"Увеличитвается на {round((1 - pred) * 100, 2)} %"
            return redirect(url_for('predict',pred=pred),code=307)
        elif request.form['submit_button'] == 'Добавить':
            zona = request.form.get('zone')
            # запрос к данным формы
            data = request.form.get('data')
            d = zona  +" "+ str(data)+" "+'\n'
            my_file = open("new.txt", 'a')
            my_file.writelines(d)

            my_file.close()
            my_file = open("new.txt",'r')
            my_string = my_file.readlines()
            my_file.close()


            return render_template('home.html',data=my_string)
        elif request.form['submit_button'] == 'Очистить':
            my_file = open("new.txt", 'w')
            my_file.close()
            my_file = open("new.txt", 'r')
            my_string = my_file.readlines()
            my_file.close()
            return render_template('home.html',data=my_string)
        elif request.form['submit_button'] == 'Пред день':
            return render_template('home.html')






    else:
        return render_template('home.html')

@app.route('/predict/<pred>',methods=['GET', 'POST'])
def predict(pred):
    #return 'welcome %s' % zona

    return  render_template('predict.html',pred=pred)

if __name__ == '__main__':
    app.run(debug=True)