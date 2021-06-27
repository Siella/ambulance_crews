#import Flask
import io
import datetime
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

def get_9H_df (file_path, column_name):
  data = pd.read_csv(file_path)
  data = data[['date', column_name]]
  data['date'] = pd.to_datetime(data['date'])
  data = data.set_index('date', drop=True)

  start = datetime.datetime(2021, 1, 1, 9, 0, 0)
  end = datetime.datetime(2021, 3, 30, 21, 0, 0)

  # Create bins
  bins = pd.date_range(start, end, freq='12H')
  data["bins"] = pd.cut(data.index, bins=bins)

  # Count grouped observations
  data = data.groupby("bins").sum()#.rename(columns={"datetime": "counts"})

  #data.index[0].left.date()
  arr = []
  days = []
  nights = []
  for d in data.index:
    if (d.left.hour == 9):
      days.append(1)
      nights.append(0)
    else:
      days.append(0)
      nights.append(1)
    arr.append(d.left.date())

  data['date'] = arr
  data['date'] = pd.to_datetime(data['date'])
  data['day'] = days
  data['night'] = nights
  data = data.set_index('date',drop=True)
  days = data[data['day']==1]
  nights = data[data['night']==1]
  return days, nights


def get_file(column_name,station):
	return column_name+'_'+station+'.csv'


bootstrap = Bootstrap(app)
@app.route('/',methods=['GET', 'POST'])
def home():
    if request.method=='POST':
        if request.form['submit_button'] == 'Пред. День':
            my_file = open("new.txt", 'r')
            my_string = my_file.readlines()
            my_file.close()
            for string in my_string:
                column_name = request.form.get('param')
                station = request.form.get('zone')
				#ЗДЕСЬ С САЙТА column_name, station , date
                date = DT.datetime.strptime(request.form.get('data'), '%Y-%m-%d')
				
				#if smena:

                name = get_file(column_name,station)
                days, nights = get_9H_df(name,column_name)
                days = days[(days.index > date - timedelta(days=7)) & (days.index < date + timedelta(days=7))][column_name]
                nights = nights[(nights.index > date - timedelta(days=7)) & (nights.index < date + timedelta(days=7))][column_name]
                #PLOT
                fig = plt.figure(figsize=(10, 5), dpi=125)
                myFmt = mdates.DateFormatter('%m-%d')
                plt.gca().xaxis.set_major_formatter(myFmt)
                plt.ylabel("Вызовы по " + column_name)
                plt.xlabel("Дата")
                plt.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
                plt.xticks(rotation=45)

                plt.plot(days.index, days, '-b', label='Дневная смена')
                plt.plot(nights.index, nights, '--r', label='Ночная смена')

                #plt.scatter(index, row, label='predict',c='#ff0000')
                plt.legend()
                plt.savefig('static/images/sdf.png')

                first_days = days.iloc[:6]
                second_days = days.iloc[7:]

                first_nights = nights.iloc[:6]
                second_nights = nights.iloc[7:]

                total_f = first_days.sum() + first_nights.sum()
                total_s = second_days.sum() + second_nights.sum()
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