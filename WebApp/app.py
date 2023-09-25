import bot

from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_data')
def get_data():
    value = get_value()
    return jsonify({'value': value})

def get_value():
    return bot.gen_word_webapp()

if __name__ == '__main__':
      app.run(debug=True)
