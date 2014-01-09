#!/usr/bin/python

from login import login
import twitterInfo as tt
import amazonwebscrape as az
from flask import Flask, jsonify, request, render_template

client = login()
azClient = az.getAccessToken()

app = Flask(__name__,static_url_path='')

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/second')
def second():
    return render_template('second.html')

@app.route('/twitter/direct')
def directInfo():
    term = request.args.get('q')    
    data = tt.getDirectInfo(client, term)        
    return jsonify(dict(data=data))

@app.route('/twitter/secondary')
def secondary():
    term = request.args.get('q')    
    data = tt.getSecondaryInfo(client, term)        
    return jsonify(dict(data=data))

@app.route('/amazon/direct')
def azInfo():
    term = request.args.get('q')    
    data = az.amazon(azClient,term)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug='True', host='0.0.0.0')
