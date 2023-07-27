import json
from PIL import PngImagePlugin
from datetime import date
from pathlib import Path
from tqdm import tqdm
import os
import webuiapi
import argostranslate.translate
import requests

def genImage(article, output_path):

    negative_prompt = "CyberRealistic_Negative, ((worst quality, low quality), bad_pictures, negative_hand-neg:1.2)"

    result = sdapi.txt2img(
        prompt=article["prompt"],
        negative_prompt=negative_prompt,
        steps=24,
        width=911,
        height=512,
        sampler_name="DPM++ 2M SDE Karras",
        restore_faces=True
        )

    image = result.image

    pnginfo = PngImagePlugin.PngInfo()
    for key in result.info:
        pnginfo.add_text(key,str(result.info[key]))

    path = Path(f"{output_path}/image_{article['sophoraId']}.png")
    path.touch()

    image.save(path, pnginfo=pnginfo)

    return path


def get_articles(path):

    if not os.path.exists(f"{path}/articles.json"):

        print("Getting todays news from api...")

        url = 'https://www.tagesschau.de/api2/homepage/'
        headers = {'accept': 'application/json'}

        response = requests.get(url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()  # Convert response to JSON format
        else:
            print(f"Request failed with status code: {response.status_code}")

        with open(f"{path}/articles.json", "w") as file:
            json.dump(data, file, indent=4)

    else:

        print(f"Getting todays news from {path}/articles.json...")

        with open(f"{path}/articles.json") as file:
            data = json.load(file)

    return data["news"]

def translate_headlines(articles):
    for article in articles:
        article["prompt"] = argostranslate.translate.translate(article["title"], "de", "en")
    return articles

def create_today_images():

    date_today = date.today().strftime("%Y/%m/%d")

    print(f"today is {date_today}")

    path = Path(f"static/images/{date_today}")
    path.mkdir(parents=True, exist_ok=True)

    articles = get_articles(path)

    translated_articles = translate_headlines(articles)

    print(f"got {len(translated_articles)} headlines")

    filtered_articles = []

    for article in tqdm(translated_articles):

        img_path = genImage(article, path)

        web_path = img_path.relative_to("static/")

        print(f"\ncreated image for:\n{article['title']}\n")

        filtered_articles.append({
            "sophoraId": article["sophoraId"],
            "title": article["title"],
            "prompt": article["prompt"],
            "path": str(web_path),
        })


    with open(path.joinpath("articles.json"), "w") as file:
        json.dump({"news":filtered_articles}, file)

    with open(path.joinpath("articles_hr.json"), "w") as file:
        json.dump({"news":filtered_articles}, file, indent=4)

if __name__ == "__main__":

    sdapi = webuiapi.WebUIApi()

    create_today_images()