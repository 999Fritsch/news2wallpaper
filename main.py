import json
from PIL import Image, PngImagePlugin
from datetime import date
from pathlib import Path
from tqdm import tqdm
from newsapi import NewsApiClient
import os
from dotenv import load_dotenv
import webuiapi

def genImage(prompt, output_path):

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

    path = Path(f"{output_path}/image_{image_name}.png")
    path.touch()

    image.save(path, pnginfo=pnginfo)


def get_articles(path, amount):

    if not os.path.exists(f"{path}/articles.json"):

        print("Getting todays news from api...")

        # Init
        newsapi = NewsApiClient(api_key=os.getenv('NEWS_API_KEY'))

        # /v2/top-headlines
        top_articles = newsapi.get_top_headlines(
                                            page_size=amount,
                                            language="de"
                                              )

        with open(f"{path}/articles.json", "w") as file:
            json.dump(top_articles, file, indent=4)

    else:

        print(f"Getting todays news from {path}/articles.json...")

        with open(f"{path}/articles.json") as file:
            top_articles = json.load(file)

    return top_articles["articles"]

def filter_articles(articles_file, output_file=None, authors_file="authors.json"):

    if output_file == None:
        output_file = articles_file

    with open(articles_file) as file:
            top_articles = json.load(file)

    with open(authors_file) as file:
            authors_filter = json.load(file)

    # Filter articles based on author and convert to a dictionary
    filtered_articles = []

    for article in top_articles["articles"]:
        if article["author"] in authors_filter["authors"]:
            filtered_articles.append(article)

    with open(f"{output_file}", "w") as file:
            json.dump({"articles":filtered_articles}, file, indent=4)

    return filtered_articles


def create_today_images():

    date_today = date.today().strftime("%Y/%m/%d")

    print(f"today is {date_today}")

    path = Path(f"images/{date_today}")
    path.mkdir(parents=True, exist_ok=True)

    get_articles(path, 100)

    filtered_articles = filter_articles(path.joinpath("articles.json"))

    print(f"got {len(filtered_articles)} headlines")

    for article in tqdm(filtered_articles):

        genImage(article["title"], path)

        print(f"\ncreated image for:\n{article['title']}\n")

if __name__ == "__main__":

    sdapi = webuiapi.WebUIApi()

    load_dotenv()

    # create_today_images()

    # genImage("cute cat", date.today().strftime("%Y/%m/%d"))

    # filter_articles("test/articles.json", "authors copy.json", "test/filtered_articles.json")

    create_today_images()