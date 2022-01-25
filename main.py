import json
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


def crawl_wiki(
        page_url: str = "https://ru.wikipedia.org/wiki/Веб-скрейпинг", resp_json: str = "data/wiki_parsing.json"
):
    print(f"page_url {page_url}, resp_json {resp_json}")
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    response_data = {
        "русский": serialize_page_version(page_url, soup)
    }

    # for every language in most common language list - serialize page
    for language in soup.find_all('a', class_='interlanguage-link-target'):
        language_page_url = language["href"]
        language_resp = requests.get(language_page_url)
        laguage_soup_page = BeautifulSoup(language_resp.text, 'html.parser')
        response_data[
            language["title"].split(" — ")[1]
        ] = serialize_page_version(language_page_url, laguage_soup_page)

    with open(resp_json, "w") as output:
        json.dump(response_data, output, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    import sys

    params = sys.argv[1:]
    crawl_wiki(*params)
