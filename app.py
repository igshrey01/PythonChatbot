from flask import Flask, render_template, request
from pyngrok import ngrok
from chatgui import *
from flask import jsonify

app = Flask(__name__)
public_url = ngrok.connect(5000).public_url
@app.route("/")
def home():
    return render_template('homepage.html',url=public_url)


@app.route('/chatbot', methods=["GET", "POST"])
def chatbotResponse():
    if request.method == 'POST':
        the_question = request.form['question']
        response = chatbot_response(the_question)
        return jsonify({"response": response })