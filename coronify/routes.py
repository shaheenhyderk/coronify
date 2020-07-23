from coronify import app
from flask import render_template, url_for, session, request
import requests
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField


@app.route('/', methods=['GET','POST'])
@app.route('/home', methods=['GET','POST'])
def home():
    if not 'state' in session:
        session['state']='KL'
    if not 'area_chart_type' in session:
        session['area_chart_type']='delta'
    form = Selform()
    if request.method == "POST":
        if request.form['button']=='ss':
            session['state']= str(form.sel_state.data)
        if request.form['button']=='pcd':
            session['area_chart_type']='delta'
        if request.form['button']=='tc':
            session['area_chart_type']='total'
    elif request.method == 'GET':
        form.sel_state.data = session['state']

    data = requests.get('https://api.covid19india.org/v4/data-all.json')
    data = data.json()

    dates=[]
    cases=[]
    for a,b in data.items():
        try:
            cases.append(str(data[a][session['state']][session['area_chart_type']]['confirmed']))
            dates.append(a)
        except:
            pass
    states=['AN', 'AP', 'AR', 'AS', 'BR', 'CH', 'CT', 'DL', 'DN', 'GA', 'GJ', 'HP', 'HR', 'JH', 'JK', 'KA', 'KL', 'LA', 'MH', 'ML', 'MN', 'MP', 'MZ', 'NL', 'OR', 'PB', 'PY', 'RJ', 'SK', 'TG', 'TN', 'TR', 'UP', 'UT', 'WB']
    statesdict={'TT':'India', 'AN': 'Andaman and Nicobar Islands', 'AP': 'Andhra Pradesh', 'AR': 'Arunachal Pradesh', 'AS': 'Assam', 'BR': 'Bihar', 'CH': 'Chandigarh', 'CT': 'Chhattisgarh', 'DL': 'Delhi', 'DN': 'Dadra and Nagar Haveli and Daman and Diu', 'GA': 'Goa', 'GJ': 'Gujarat', 'HP': 'Himachal Pradesh', 'HR': 'Haryana', 'JH': 'Jharkhand', 'JK': 'Jammu and Kashmir', 'KA': 'Karnataka', 'KL': 'Kerala', 'LA': 'Ladakh', 'MH': 'Maharashtra', 'ML': 'Meghalaya', 'MN': 'Manipur', 'MP': 'Madhya Pradesh', 'MZ': 'Mizoram', 'NL': 'Nagaland', 'OR': 'Odisha', 'PB': 'Punjab', 'PY': 'Puducherry', 'RJ': 'Rajasthan', 'SK': 'Sikkim', 'TG': 'Telangana', 'TN': 'Tamil Nadu', 'TR': 'Tripura', 'UP': 'Uttar Pradesh', 'UT': 'Uttarakhand', 'WB': 'West Bengal'}

    total_india = data[dates[-1]]['TT']['total']['confirmed']
    total_pop_india = data[dates[-1]]['TT']['meta']['population']
    total_percentage_india = total_india*100/total_pop_india
    total_percentage_india = round(total_percentage_india,3)

    total_state = data[dates[-1]][session['state']]['total']['confirmed']
    total_pop_state = data[dates[-1]][session['state']]['meta']['population']
    total_percentage_state = total_state*100/total_pop_state
    total_percentage_state = round(total_percentage_state,3)

    today_india = data[dates[-1]]['TT']['delta']['confirmed']
    today_state = data[dates[-1]][session['state']]['delta']['confirmed']

    if session['state'] == 'TT':
        total_dist=[]
        for i in states:
            try:
                temp_list=[statesdict[i],data[dates[-1]][i]['total']['confirmed']]
                total_dist.append(temp_list)
            except:
                pass
        total_dist.sort(key = lambda x: x[1],reverse=True)
        high_dist_value=total_dist[0][1]
        for i in range(len(total_dist)):
            percent= int(total_dist[i][1]*100/high_dist_value)
            total_dist[i].append(percent)

        delta_dist=[]
        for i in states:
            try:
                temp_list=[statesdict[i],data[dates[-1]][i]['delta']['confirmed']]
                delta_dist.append(temp_list)
            except:
                pass
        delta_dist.sort(key = lambda x: x[1],reverse=True)
    
    else:
        total_dist=[]
        for i,j in data[dates[-1]][session['state']]['districts'].items():
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
        for i,j in data[dates[-1]][session['state']]['districts'].items():
            try:
                temp_list=[i,j['delta']['confirmed']]
                delta_dist.append(temp_list)
            except:
                pass
        delta_dist.sort(key = lambda x: x[1],reverse=True)

    total_india = "{:,}".format(total_india)
    total_state = "{:,}".format(total_state)
    total_pop_india = "{:,}".format(total_pop_india)
    total_pop_state = "{:,}".format(total_pop_state)
    today_india = "{:,}".format(today_india)
    today_state = "{:,}".format(today_state)
    
    return render_template('index.html', form=form, state=statesdict[session['state']], total_india=total_india, total_state=total_state, total_pop_india=total_pop_india, total_pop_state=total_pop_state, total_percentage_india=total_percentage_india, total_percentage_state=total_percentage_state, today_india=today_india, today_state=today_state, dates=dates, cases=cases, total_dist=total_dist, delta_dist=delta_dist, last_updated=dates[-1])

class Selform(FlaskForm):
    sel_state = SelectField('sel_state', choices=[('TT','India'),('AN', 'Andaman and Nicobar Islands'), ('AP', 'Andhra Pradesh'), ('AR', 'Arunachal Pradesh'), ('AS', 'Assam'), ('BR', 'Bihar'), ('CH', 'Chandigarh'), ('CT', 'Chhattisgarh'), ('DL', 'Delhi'), ('DN', 'Dadra and Nagar Haveli and Daman and Diu'), ('GA', 'Goa'), ('GJ', 'Gujarat'), ('HP', 'Himachal Pradesh'), ('HR', 'Haryana'), ('JH', 'Jharkhand'), ('JK', 'Jammu and Kashmir'), ('KA', 'Karnataka'), ('KL', 'Kerala'), ('LA', 'Ladakh'), ('MH', 'Maharashtra'), ('ML', 'Meghalaya'), ('MN', 'Manipur'), ('MP', 'Madhya Pradesh'), ('MZ', 'Mizoram'), ('NL', 'Nagaland'), ('OR', 'Odisha'), ('PB', 'Punjab'), ('PY', 'Puducherry'), ('RJ', 'Rajasthan'), ('SK', 'Sikkim'), ('TG', 'Telangana'), ('TN', 'Tamil Nadu'), ('TR', 'Tripura'), ('UP', 'Uttar Pradesh'), ('UT', 'Uttarakhand'), ('WB', 'West Bengal')])
