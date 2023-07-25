import json
from PIL import Image, PngImagePlugin
from datetime import date
from pathlib import Path
from tqdm import tqdm
from newsapi import NewsApiClient
import os
from dotenv import load_dotenv
import webuiapi

def get_unique_authors(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        
    authors = {article['author'] for article in data['articles']}
    unique_authors = list(authors)
    return unique_authors

def get_sources():

    load_dotenv()

    news = NewsApiClient(api_key=os.getenv('NEWS_API_KEY'))

    sources = news.get_sources(country="de")

    with open(f"sources_ger.json", "w") as file:
        json.dump(sources, file, indent=4)

authors = get_unique_authors("articles.json")

with open(f"authors.json", "w") as file:
        json.dump(authors, file, indent=4, ensure_ascii=False)