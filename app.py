import numpy as np
from flask import Flask, request, render_template
from flask_cors import CORS
import os
import joblib
import pickle
import flask
import os
import newspaper
from newspaper import Article
import urllib

app = Flask(__name__)
CORS(app)
app = flask.Flask(__name__, template_folder='templates', static_url_path='/static')
with open('model.pickle', 'rb') as handle:
    model = pickle.load(handle)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/Predicted', methods=['GET','POST'])
def predict():
    url = request.get_data(as_text=True)[5:]
    url = urllib.parse.unquote(url)
    article = Article(str(url))
    article.download()
    article.parse()
    article.nlp()
    news = article.summary
    pred = 'Authentic' if(model.predict([news])) else 'Fake'
    return render_template('main.html', prediction_text=f'The news is {pred}')

if __name__=="__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port, debug=True, use_reloader=True)
