import json
from pymongo import MongoClient
from typing import Dict, Any

import requests
from bs4 import BeautifulSoup


def serialize_page_version(page_url: str, page_obj: BeautifulSoup) -> Dict[str, Any]:
    """
    Create dictionary from `BeautifulSoup` page object.
    """
    data = {
        "title": page_obj.title.string,
        "content_anchor_links": [],
        "content": page_obj.find(
            "div", {
                "id": "mw-content-text"
            }).get_text(),
        "external_links": [],
    }

    for link in page_obj.find_all("li", class_="toclevel-1"):
        data["content_anchor_links"].append(
            f"{page_url}{link.find('a')['href']}"
        )

    data["external_links"] = [
        link["href"] for link in page_obj.find(
            "div", {"id": "mw-content-text"}
        ).find_all("a", class_="external")
    ]

    data["external_links"] = list(
        map(lambda x: x[2:] if x.startswith("//") else x, data["external_links"])
    )

    return data


def crawl_wiki(db, page_url):
    print(f"page_url {page_url}")
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    response_data = {
        "русский": serialize_page_version(page_url, soup)
    }

    # for every language in most common language list - serialize page
    for language in soup.find_all('a', class_='interlanguage-link-target'):
        print("Language", language["href"])
        language_page_url = language["href"]
        language_resp = requests.get(language_page_url)
        laguage_soup_page = BeautifulSoup(language_resp.text, 'html.parser')
        response_data[
            language["title"].split(" — ")[1]
        ] = serialize_page_version(language_page_url, laguage_soup_page)

    article_id = db.articles.insert_one(response_data).inserted_id
    print("Article id", article_id)


if __name__ == "__main__":
    import os

    client = MongoClient('mongodb', 27017)
    db = client.texts
    page_url = os.environ["PAGE_URL"] or "https://ru.wikipedia.org/wiki/Веб-скрейпинг"

    crawl_wiki(db, page_url)
