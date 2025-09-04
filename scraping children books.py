import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

base_url = "https://openlibrary.org/search?subject=Juvenile+fiction&page="
api_base_url = "https://openlibrary.org"

title_children_list = []
author_children_list = []
want_to_rea_children_list = []
publish_year_children_list = []
rating_children_list = []
num_rating_children_list = []
num_edition_children_list = []
book_ur_children_list = []

isb_children_list = []
num_page_children_list = []
publisher_children_list = []
subject_children_list = []
language_children_list = []
key_children_list = []

def scrape_book_children(page_limit):
    for page in range(1, page_limit + 1):
        print(f"Scrapin_children page {page}...")
        url = base_url + str(page)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        books = soup.find_all('div', class_='details')

        for book in books:
            title = book.find('h3', class_='booktitle')
            title_children_list.append(title.a.text.strip() if title and title.a else "N/A")

            author = book.find('span', class_='bookauthor')
            author_children_list.append(author.a.text.strip() if author and author.a else "N/A")

            want_to_read = book.find('span', {'class': 'ratingsByline', 'itemprop': 'reviewCount'})
            number = re.sub(r"[^\d]", "", want_to_read.text.strip()) if want_to_read else "N/A"
            want_to_rea_children_list.append(number)

            result_details = book.find('span', class_='resultDetails')
            if result_details and "First published in" in result_details.text:
                year_match = re.search(r"First published in.*?(\b\d{4}\b)", result_details.text)
                year = year_match.group(1) if year_match else "N/A"
                publish_year_children_list.append(year)
            else:
                publish_year_children_list.append("N/A")

            ratings_byline = book.find('span', class_='ratingsByline')
            if ratings_byline:
                rating_info = ratings_byline.text.strip()
                match = re.search(r"([\d.]+)\s+\((\d+)\s+ratings?\)", rating_info)
                if match:
                    rating_children_list.append(match.group(1))
                    num_rating_children_list.append(match.group(2))
                else:
                    rating_children_list.append("N/A")
                    num_rating_children_list.append("N/A")
            else:
                rating_children_list.append("N/A")
                num_rating_children_list.append("N/A")

            editions = book.find('a', text=lambda x: x and "edition" in x.lower())
            number_of_editions = re.sub(r"[^0-9]", "", editions.text.strip()) if editions else "N/A"
            num_edition_children_list.append(number_of_editions)

            book_link = book.find('h3', class_='booktitle')
            book_url = api_base_url + book_link.a['href'] if book_link and book_link.a else "N/A"
            book_ur_children_list.append(book_url)

def fetch_book_detail_children(book_url_list):
    for book_url in book_url_list:
        if book_url == "N/A":
            isb_children_list.append("N/A")
            num_page_children_list.append("N/A")
            publisher_children_list.append("N/A")
            subject_children_list.append("N/A")
            language_children_list.append("N/A")
            key_children_list.append("N/A")
            continue

    #######################
        book_key = book_url.split('/')[-1]
        api_url = f"{api_base_url}/works/{book_key}.json"

        try:
            response = requests.get(api_url)
            if response.status_code != 200:
                raise Exception(f"Failed to fetch API data for {book_url}")

            data = response.json()

            isb_children_list.append(", ".join(data.get("isbn_10", ["N/A"])))

            num_page_children_list.append(data.get("number_of_pages", "N/A"))

            publisher_children_list.append(", ".join(data.get("publishers", ["N/A"])))

            subject_children_list.append(", ".join(data.get("subjects", ["N/A"])))

            language_children_list.append(", ".join(lang.get("key", "").split("/")[-1] for lang in data.get("languages", [])))

            key_children_list.append(data.get("key", "N/A"))

        except Exception as e:
            print(f"Error fetching API data for {book_url}: {e}")
            isb_children_list.append("N/A")
            num_page_children_list.append("N/A")
            publisher_children_list.append("N/A")
            subject_children_list.append("N/A")
            language_children_list.append("N/A")
            key_children_list.append("N/A")


scrape_book_children(page_limit=50)  
fetch_book_detail_children(book_ur_children_list)

d_children = pd.DataFrame({
    "Title": title_children_list,
    "Authors": author_children_list,
    "Number of People Who Want to Read": want_to_rea_children_list,
    "First Published Year": publish_year_children_list,
    "Ratings": rating_children_list,
    "Number of Ratings": num_rating_children_list,
    "Number of Editions": num_edition_children_list,
    "Book URL": book_ur_children_list,
    "ISBN": isb_children_list,
    "Number of Pages": num_page_children_list,
    "Publishers": publisher_children_list,
    "Subjects": subject_children_list,
    "Languages": language_children_list,
    "Key": key_children_list
})

d_children.to_csv('1000_children books.csv', index=False)

print("children data saved to 1000_children_books.csv'")
