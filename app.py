from flask import Flask, render_template, jsonify, request  
import json
import time

app = Flask(__name__)

def load_data():
    with open('static/images/2023/07/27/articles.json') as f:
        data = json.load(f)
    return data['news']

@app.route('/')
def index():
    return render_template('news.html')

@app.route('/get_news_data')
def get_news_data():
    news_items = load_data()
    current_item_index = int(request.args.get('current_item_index', 0))
    current_item = news_items[current_item_index]
    title = current_item['title']
    image_path = current_item['path']
    next_item_index = (current_item_index + 1) % len(news_items)
    return jsonify({'title': title, 'image_path': image_path, 'next_item_index': next_item_index})

if __name__ == '__main__':
    app.run()
