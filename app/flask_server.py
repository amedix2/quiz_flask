import json
import logging
import sys

from flask import Flask, jsonify, render_template

__all__ = ['app']

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/update_data', methods=['GET'])
def update_data():
    data = json.load(open('static/data/players.json', 'r', encoding='utf-8'))
    return jsonify(data)


@app.route('/question/<int:num>')
def questions(num):
    logging.info(str(num))
    data = json.load(open('static/data/questions.json', 'r', encoding='utf-8'))
    try:
        question_data = data[str(num)]
        data['current'] = str(num)
        open('static/data/questions.json', 'w', encoding='utf-8').write(
            json.dumps(data),
        )
        return render_template(
            'question.html',
            num=num,
            data=json.dumps(question_data),
        )
    except Exception:
        raise ValueError


@app.route('/results')
def results():
    data = json.load(open('static/data/players.json', 'r', encoding='utf-8'))
    zero_data = data
    logging.info(data)
    for player in zero_data.keys():
        zero_data[player]['given'] = False
    open('static/data/players.json', 'w', encoding='utf-8').write(
        json.dumps(zero_data),
    )
    # new num question
    num_data = json.load(
        open('static/data/questions.json.', 'r', encoding='utf-8'),
    )
    num_data['current'] = str(int(num_data['current']) + 1)
    next_num = num_data['current']
    open('static/data/questions.json', 'w', encoding='utf-8').write(
        json.dumps(num_data),
    )
    return render_template('results.html', data=data, num=next_num)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    app.run(debug=True, host='127.0.0.1', port=80)
