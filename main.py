import json
from pprint import pprint
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import unicodedata
from vacancy_currency import main_vacancy


def search_vacancies_by_keywords(keywords: str, pages: int, v=None):
    url = "https://spb.hh.ru/search/vacancy"
    vacancies = dict(vacancies=[])

    for j in range(pages):
        headers = Headers(os="win", browser="chrome")
        params = {
            "text": keywords,
            "area": ["1", "2"],
            "search_field": ["name", "description"],
            "page": j,
        }
        response_main = requests.get(url, headers=headers.generate(), params=params)
        soup_main = BeautifulSoup(response_main.text, "lxml")
        vacancy_results = soup_main.find_all("div", class_="vacancy-serp-item__layout")

        for vacancy in vacancy_results:
            try:
                vacancy_name = (
                    vacancy.find(
                        "span",
                        {"data-page-analytics-event": "vacancy_search_suitable_item"},
                    )
                    .find("a")
                    .text
                )
                vacancy_href = vacancy.find("a").get("href")
                vacancy_search_compensation = vacancy.find(
                    "span", {"data-qa": "vacancy-serp__vacancy-compensation"}
                )
                if vacancy_search_compensation:
                    vacancy_compensation = vacancy_search_compensation.text
                else:
                    vacancy_compensation = " "
                vacancy_company = (
                    vacancy.find("div", class_="vacancy-serp-item__meta-info-company")
                    .find("a")
                    .text
                )
                vacancy_city = (
                    vacancy.find("div", {"data-qa": "vacancy-serp__vacancy-address"})
                    .text.split()[0]
                    .strip(",")
                )
                information_vacancy = dict(
                    name=vacancy_name,
                    link=vacancy_href,
                    compensation=unicodedata.normalize("NFKD", vacancy_compensation),
                    company=unicodedata.normalize("NFKD", vacancy_company),
                    city=vacancy_city,
                )
                vacancies["vacancies"].append(information_vacancy)
            except Exception as exp:
                print(exp)
    return vacancies


def write_json(file: dict):
    with open("vacancies.json", "w", encoding="utf-8") as f:
        json.dump(file, f, ensure_ascii=False)
    return "Successfully: main.py"


def main():
    keywords = "python flask django"
    pages = 2
    data = search_vacancies_by_keywords(keywords, pages)
    print(write_json(data))
    pprint(data, sort_dicts=False)


if __name__ == "__main__":
    main()
    print()
    main_vacancy()
