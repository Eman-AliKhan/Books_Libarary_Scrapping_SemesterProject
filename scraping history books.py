import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

base_url = "https://openlibrary.org/search?subject=History&page="
api_base_url = "https://openlibrary.org"

titles_history_list = []
authors_history_list = []
want_to_read_history_list = []
publish_years_history_list = []
ratings_history_list = []
num_ratings_history_list = []
num_editions_history_list = []
book_url_history_list = []

isbn_history_list = []
num_pages_history_list = []
publishers_history_list = []
subjects_history_list = []
languages_history_list = []
keys_history_list = []

def scrape_books_history(page_limit):
    for page in range(1, page_limit + 1):
        print(f"Scraping history page {page}...")
        url = base_url + str(page)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        books = soup.find_all('div', class_='details')

        for book in books:
            title = book.find('h3', class_='booktitle')
            titles_history_list.append(title.a.text.strip() if title and title.a else "N/A")

            author = book.find('span', class_='bookauthor')
            authors_history_list.append(author.a.text.strip() if author and author.a else "N/A")

            want_to_read = book.find('span', {'class': 'ratingsByline', 'itemprop': 'reviewCount'})
            number = re.sub(r"[^\d]", "", want_to_read.text.strip()) if want_to_read else "N/A"
            want_to_read_history_list.append(number)

            result_details = book.find('span', class_='resultDetails')
            if result_details and "First published in" in result_details.text:
                year_match = re.search(r"First published in.*?(\b\d{4}\b)", result_details.text)
                year = year_match.group(1) if year_match else "N/A"
                publish_years_history_list.append(year)
            else:
                publish_years_history_list.append("N/A")

            ratings_byline = book.find('span', class_='ratingsByline')
            if ratings_byline:
                rating_info = ratings_byline.text.strip()
                match = re.search(r"([\d.]+)\s+\((\d+)\s+ratings?\)", rating_info)
                if match:
                    ratings_history_list.append(match.group(1))
                    num_ratings_history_list.append(match.group(2))
                else:
                    ratings_history_list.append("N/A")
                    num_ratings_history_list.append("N/A")
            else:
                ratings_history_list.append("N/A")
                num_ratings_history_list.append("N/A")

            editions = book.find('a', text=lambda x: x and "edition" in x.lower())
            number_of_editions = re.sub(r"[^0-9]", "", editions.text.strip()) if editions else "N/A"
            num_editions_history_list.append(number_of_editions)

            book_link = book.find('h3', class_='booktitle')
            book_url = api_base_url + book_link.a['href'] if book_link and book_link.a else "N/A"
            book_url_history_list.append(book_url)

def fetch_book_details_history(book_url_list):
    for book_url in book_url_list:
        if book_url == "N/A":
            isbn_history_list.append("N/A")
            num_pages_history_list.append("N/A")
            publishers_history_list.append("N/A")
            subjects_history_list.append("N/A")
            languages_history_list.append("N/A")
            keys_history_list.append("N/A")
            continue

    ####################
        book_key = book_url.split('/')[-1]
        api_url = f"{api_base_url}/works/{book_key}.json"

        try:
            response = requests.get(api_url)
            if response.status_code != 200:
                raise Exception(f"Failed to fetch API data for {book_url}")

            data = response.json()

            isbn_history_list.append(", ".join(data.get("isbn_10", ["N/A"])))

            num_pages_history_list.append(data.get("number_of_pages", "N/A"))

            publishers_history_list.append(", ".join(data.get("publishers", ["N/A"])))

            subjects_history_list.append(", ".join(data.get("subjects", ["N/A"])))

            languages_history_list.append(", ".join(lang.get("key", "").split("/")[-1] for lang in data.get("languages", [])))

            keys_history_list.append(data.get("key", "N/A"))

        except Exception as e:
            print(f"Error fetching API data for {book_url}: {e}")
            isbn_history_list.append("N/A")
            num_pages_history_list.append("N/A")
            publishers_history_list.append("N/A")
            subjects_history_list.append("N/A")
            languages_history_list.append("N/A")
            keys_history_list.append("N/A")


scrape_books_history(page_limit=50)  
fetch_book_details_history(book_url_history_list)

df_history = pd.DataFrame({
    "Title": titles_history_list,
    "Authors": authors_history_list,
    "Number of People Who Want to Read": want_to_read_history_list,
    "First Published Year": publish_years_history_list,
    "Ratings": ratings_history_list,
    "Number of Ratings": num_ratings_history_list,
    "Number of Editions": num_editions_history_list,
    "Book URL": book_url_history_list,
    "ISBN": isbn_history_list,
    "Number of Pages": num_pages_history_list,
    "Publishers": publishers_history_list,
    "Subjects": subjects_history_list,
    "Languages": languages_history_list,
    "Key": keys_history_list
})

df_history.to_csv('1000 history books.csv', index=False)

print("history data saved to 'history_books.csv'")
