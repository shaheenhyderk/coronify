from coronify import app
from flask import render_template, url_for, session, request
import requests
import json
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

state='KL'
area_chart_type='delta'

@app.route('/', methods=['GET','POST'])
@app.route('/home', methods=['GET','POST'])
def home():
    global state
    global area_chart_type
    form = Selform()
    if request.method == "POST":
        if request.form['button']=='ss':
            state= str(form.state.data)
        if request.form['button']=='pcd':
            area_chart_type='delta'
        if request.form['button']=='tc':
            area_chart_type='total'

    data = requests.get('https://api.covid19india.org/v4/data-all.json')
    data = data.json()

    dates=[]
    cases=[]
    for a,b in data.items():
        try:
            cases.append(str(data[a][state][area_chart_type]['confirmed']))
            dates.append(a)
        except:
            pass
    states=['AN', 'AP', 'AR', 'AS', 'BR', 'CH', 'CT', 'DL', 'DN', 'GA', 'GJ', 'HP', 'HR', 'JH', 'JK', 'KA', 'KL', 'LA', 'MH', 'ML', 'MN', 'MP', 'MZ', 'NL', 'OR', 'PB', 'PY', 'RJ', 'SK', 'TG', 'TN', 'TR', 'TT', 'UP', 'UT', 'WB']
    statesdict={'AN': 'Andaman and Nicobar Islands', 'AP': 'Andhra Pradesh', 'AR': 'Arunachal Pradesh', 'AS': 'Assam', 'BR': 'Bihar', 'CH': 'Chandigarh', 'CT': 'Chhattisgarh', 'DL': 'Delhi', 'DN': 'Dadra and Nagar Haveli and Daman and Diu', 'GA': 'Goa', 'GJ': 'Gujarat', 'HP': 'Himachal Pradesh', 'HR': 'Haryana', 'JH': 'Jharkhand', 'JK': 'Jammu and Kashmir', 'KA': 'Karnataka', 'KL': 'Kerala', 'LA': 'Ladakh', 'MH': 'Maharashtra', 'ML': 'Meghalaya', 'MN': 'Manipur', 'MP': 'Madhya Pradesh', 'MZ': 'Mizoram', 'NL': 'Nagaland', 'OR': 'Odisha', 'PB': 'Punjab', 'PY': 'Puducherry', 'RJ': 'Rajasthan', 'SK': 'Sikkim', 'TG': 'Telangana', 'TN': 'Tamil Nadu', 'TR': 'Tripura', 'UP': 'Uttar Pradesh', 'UT': 'Uttarakhand', 'WB': 'West Bengal'}

    total_india = data[dates[-1]]['TT']['total']['confirmed']
    total_state = data[dates[-1]][state]['total']['confirmed']
    today_india = data[dates[-1]]['TT']['total']['confirmed']-data[dates[-2]]['TT']['total']['confirmed']
    today_state = data[dates[-1]][state]['total']['confirmed']-data[dates[-2]][state]['total']['confirmed']

    total_dist=[]
    for i,j in data[dates[-1]][state]['districts'].items():
        try:
            temp_list=[i,j['total']['confirmed']]
            total_dist.append(temp_list)
        except:
            pass
    total_dist.sort(key = lambda x: x[1],reverse=True)
    high_dist_value=total_dist[0][1]
    for i in range(len(total_dist)):
        percent= int(total_dist[i][1]*100/high_dist_value)
        total_dist[i].append(percent)

    delta_dist=[]
    for i,j in data[dates[-1]][state]['districts'].items():
        try:
            temp_list=[i,j['delta']['confirmed']]
            delta_dist.append(temp_list)
        except:
            pass
    delta_dist.sort(key = lambda x: x[1],reverse=True)
    
    return render_template('index.html', form=form, state=statesdict[state], total_india=total_india, total_state=total_state, today_india=today_india, today_state=today_state, dates=dates, cases=cases, states=states, total_dist=total_dist, delta_dist=delta_dist)

class Selform(FlaskForm):
    state = SelectField('State', choices=[('AN', 'Andaman and Nicobar Islands'), ('AP', 'Andhra Pradesh'), ('AR', 'Arunachal Pradesh'), ('AS', 'Assam'), ('BR', 'Bihar'), ('CH', 'Chandigarh'), ('CT', 'Chhattisgarh'), ('DL', 'Delhi'), ('DN', 'Dadra and Nagar Haveli and Daman and Diu'), ('GA', 'Goa'), ('GJ', 'Gujarat'), ('HP', 'Himachal Pradesh'), ('HR', 'Haryana'), ('JH', 'Jharkhand'), ('JK', 'Jammu and Kashmir'), ('KA', 'Karnataka'), ('KL', 'Kerala'), ('LA', 'Ladakh'), ('MH', 'Maharashtra'), ('ML', 'Meghalaya'), ('MN', 'Manipur'), ('MP', 'Madhya Pradesh'), ('MZ', 'Mizoram'), ('NL', 'Nagaland'), ('OR', 'Odisha'), ('PB', 'Punjab'), ('PY', 'Puducherry'), ('RJ', 'Rajasthan'), ('SK', 'Sikkim'), ('TG', 'Telangana'), ('TN', 'Tamil Nadu'), ('TR', 'Tripura'), ('UP', 'Uttar Pradesh'), ('UT', 'Uttarakhand'), ('WB', 'West Bengal')], default='KL')
    submit= SubmitField('Search')