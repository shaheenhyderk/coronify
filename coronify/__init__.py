from flask import Flask

app=Flask(__name__)
app.config['SECRET_KEY']='xdfhf@!#$%erfndyub132542707897212###sdffj'

from coronify import routes