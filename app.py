from flask import Flask, render_template
import json
import time

app = Flask(__name__)

def load_data():
    with open('static/images/2023/07/27/articles.json') as f:
        data = json.load(f)
    return data['news']

@app.route('/')
def index():
    news_items = load_data()
    current_item_index = 0

    while True:
        current_item = news_items[current_item_index]
        title = current_item['title']
        image_path = current_item['path']

        return render_template('news.html', title=title, image_path=image_path)

        current_item_index = (current_item_index + 1) % len(news_items)
        time.sleep(120)

if __name__ == '__main__':
    app.run()
