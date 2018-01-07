import requests
import csv
from parser.Tender import Tender
try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup


def extract_tenders_from_web_page_by_url(url):
    html = requests.get(url).text
    parsed_html = BeautifulSoup(html, "html.parser")
    if is_last_page(parsed_html):
        return None
    a = parsed_html.find_all("a", {"class": "shortestProcedures__item"})
    tender_list = []
    for tender in a:
        t = Tender()
        t.link = tender['href']
        t.number = tender.find("div", {"class": "shortestProcedures__cell shortestProcedures__cell--number"}).get_text()
        t.description = tender.find("div", {"class": "shortestProcedures__cell shortestProcedures__cell--description"}).get_text()
        t.company = tender.find("span", {"class": "shortestProcedures__customerName"}).get_text()
        t.date = tender.find("span", {"class": "shortestProcedures__date"}).get_text()
        t.price = tender.find("span", {"class": "shortestProcedures__price shortestProcedures__price--noPrice"}).get_text()
        tender_list.append(t)
    return tender_list


def is_last_page(parsed_html):
    return parsed_html.find("div", {"class": "emptyResultsBlock"})


if __name__ == "__main__":
    writer = csv.writer(open("output.csv", 'w'))
    first_page = "https://etpgpb.ru/procedures/?procedure%5Bcategory%5D=all"
    tenders_list = extract_tenders_from_web_page_by_url(first_page)
    all_tenders_list = tenders_list[:]
    page_number = 2
    page_url_left = "https://etpgpb.ru/procedures/page/"
    page_url_right = "/?procedure%5Bcategory%5D=all"

    while tenders_list:
        print("Current processing page: " + str(page_number) + " Tender list size: " + str(len(all_tenders_list)))
        tenders_list = extract_tenders_from_web_page_by_url(page_url_left + str(page_number) + page_url_right)
        if tenders_list:
            all_tenders_list += tenders_list[:]
        page_number += 1
    print("Start saving to csv")
    for t in all_tenders_list:
        writer.writerow(t.to_list())
    print("Finish saving to csv")


