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
import webuiapi

def genImage(prompt, date):

    negative_prompt = "CyberRealistic_Negative, ((worst quality, low quality), bad_pictures, negative_hand-neg:1.2)"

    result = sdapi.txt2img(
        prompt=prompt,
        negative_prompt=negative_prompt,
        steps=24,
        width=512,
        height=512,
        sampler_name="DPM++ 2M SDE Karras",
        restore_faces=True
        )

    image = result.image

    pnginfo = PngImagePlugin.PngInfo()
    for key in result.info:
        pnginfo.add_text(key,str(result.info[key]))

    image_name =  ''.join(filter(str.isalnum, prompt))

    path = Path(f"images/{date}/image_{image_name}.png")
    path.touch()

    image.save(path, pnginfo=pnginfo)


def get_headlines(date):

    if not os.path.exists(f"images/{date}/articles.json"):

        print("Getting todays news from api...")

        # Init
        newsapi = NewsApiClient(api_key=os.getenv('NEWS_API_KEY'))

        # /v2/top-headlines
        top_headlines = newsapi.get_top_headlines(
                                            page_size=10,
                                            language="de"
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

    sdapi = webuiapi.WebUIApi()

    load_dotenv()

    create_today_images()

    # genImage("cute cat", date.today().strftime("%Y/%m/%d"))