import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin
from datetime import date
from pathlib import Path
from tqdm import tqdm
from newsapi import NewsApiClient
import os
from dotenv import load_dotenv

def genImage(prompt, date):
    url = "http://127.0.0.1:7860"

    payload = {
        "prompt": f"{prompt}",
        "steps": 75,
        "width": 960,
        "height": 540,
        "sampler_name": "DPM++ 2M SDE Karras",
        "negative_prompt": "CyberRealistic_Negative, ((worst quality, low quality), bad_pictures, negative_hand-neg:1.2)"
    }

    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

    r = response.json()

    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

        png_payload = {
            "image": "data:image/png;base64," + i
        }
        response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))
        image.save(f'images/{date}/image_{prompt.replace(" ","_")[:200]}.png', pnginfo=pnginfo)


def get_headlines(date):

    if not os.path.exists(f"images/{date}/articles.json"):

        print("Getting todays news from api...")

        # Init
        newsapi = NewsApiClient(api_key=os.getenv('NEWS_API_KEY'))

        # /v2/top-headlines
        top_headlines = newsapi.get_top_headlines(
                                              page_size=8,
                                              language="en"
                                              )

        with open(f"images/{date}/articles.json", "w") as file:
            json.dump(top_headlines, file, indent=4)

    else:

        print(f"Getting todays news from images/{date}/articles.json...")

        with open(f"images/{date}/articles.json") as file:
            top_headlines = json.load(file)
        
    headlines_list = []
    for article in top_headlines["articles"]:

        headlines_list.append(article["title"])

    return headlines_list

def create_today_images():

    date_today = date.today().strftime("%Y/%m/%d")

    print(f"today is {date_today}")

    Path(f"images/{date_today}").mkdir(parents=True, exist_ok=True)

    headlines = get_headlines(date_today)

    print(f"got {len(headlines)} headlines")

    for headline in tqdm(headlines):

        genImage(headline, date_today)

        print(f"\ncreated image for:\n{headline}\n")

if __name__ == "__main__":

    load_dotenv()

    create_today_images()