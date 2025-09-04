import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

base_url = "https://openlibrary.org/search?subject=Autobiography&page="
api_base_url = "https://openlibrary.org"

titles_autobio_list = []
authors_autobio_list = []
want_to_read_autobio_list = []
publish_years_autobio_list = []
ratings_autobio_list = []
num_ratings_autobio_list = []
num_editions_autobio_list = []
book_url_autobio_list = []

isbn_autobio_list = []
num_pages_autobio_list = []
publishers_autobio_list = []
subjects_autobio_list = []
languages_autobio_list = []
keys_autobio_list = []

def scrape_books_autobio(page_limit):
    for page in range(1, page_limit + 1):
        print(f"Scraping autobio page {page}...")
        url = base_url + str(page)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        books = soup.find_all('div', class_='details')

        for book in books:
            title = book.find('h3', class_='booktitle')
            titles_autobio_list.append(title.a.text.strip() if title and title.a else "N/A")

            author = book.find('span', class_='bookauthor')
            authors_autobio_list.append(author.a.text.strip() if author and author.a else "N/A")

            want_to_read = book.find('span', {'class': 'ratingsByline', 'itemprop': 'reviewCount'})
            number = re.sub(r"[^\d]", "", want_to_read.text.strip()) if want_to_read else "N/A"
            want_to_read_autobio_list.append(number)

            result_details = book.find('span', class_='resultDetails')
            if result_details and "First published in" in result_details.text:
                year_match = re.search(r"First published in.*?(\b\d{4}\b)", result_details.text)
                year = year_match.group(1) if year_match else "N/A"
                publish_years_autobio_list.append(year)
            else:
                publish_years_autobio_list.append("N/A")

            ratings_byline = book.find('span', class_='ratingsByline')
            if ratings_byline:
                rating_info = ratings_byline.text.strip()
                match = re.search(r"([\d.]+)\s+\((\d+)\s+ratings?\)", rating_info)
                if match:
                    ratings_autobio_list.append(match.group(1))
                    num_ratings_autobio_list.append(match.group(2))
                else:
                    ratings_autobio_list.append("N/A")
                    num_ratings_autobio_list.append("N/A")
            else:
                ratings_autobio_list.append("N/A")
                num_ratings_autobio_list.append("N/A")

            editions = book.find('a', text=lambda x: x and "edition" in x.lower())
            number_of_editions = re.sub(r"[^0-9]", "", editions.text.strip()) if editions else "N/A"
            num_editions_autobio_list.append(number_of_editions)

            book_link = book.find('h3', class_='booktitle')
            book_url = api_base_url + book_link.a['href'] if book_link and book_link.a else "N/A"
            book_url_autobio_list.append(book_url)

def fetch_book_details_autobio(book_url_list):
    for book_url in book_url_list:
        if book_url == "N/A":
            isbn_autobio_list.append("N/A")
            num_pages_autobio_list.append("N/A")
            publishers_autobio_list.append("N/A")
            subjects_autobio_list.append("N/A")
            languages_autobio_list.append("N/A")
            keys_autobio_list.append("N/A")
            continue

##################
        book_key = book_url.split('/')[-1]
        api_url = f"{api_base_url}/works/{book_key}.json"

        try:
            response = requests.get(api_url)
            if response.status_code != 200:
                raise Exception(f"Failed to fetch API data for {book_url}")

            data = response.json()

            isbn_autobio_list.append(", ".join(data.get("isbn_10", ["N/A"])))

            num_pages_autobio_list.append(data.get("number_of_pages", "N/A"))

            publishers_autobio_list.append(", ".join(data.get("publishers", ["N/A"])))

            subjects_autobio_list.append(", ".join(data.get("subjects", ["N/A"])))

            languages_autobio_list.append(", ".join(lang.get("key", "").split("/")[-1] for lang in data.get("languages", [])))

            keys_autobio_list.append(data.get("key", "N/A"))

        except Exception as e:
            print(f"Error fetching API data for {book_url}: {e}")
            isbn_autobio_list.append("N/A")
            num_pages_autobio_list.append("N/A")
            publishers_autobio_list.append("N/A")
            subjects_autobio_list.append("N/A")
            languages_autobio_list.append("N/A")
            keys_autobio_list.append("N/A")


scrape_books_autobio(page_limit=50)  
fetch_book_details_autobio(book_url_autobio_list)

df_autobio = pd.DataFrame({
    "Title": titles_autobio_list,
    "Authors": authors_autobio_list,
    "Number of People Who Want to Read": want_to_read_autobio_list,
    "First Published Year": publish_years_autobio_list,
    "Ratings": ratings_autobio_list,
    "Number of Ratings": num_ratings_autobio_list,
    "Number of Editions": num_editions_autobio_list,
    "Book URL": book_url_autobio_list,
    "ISBN": isbn_autobio_list,
    "Number of Pages": num_pages_autobio_list,
    "Publishers": publishers_autobio_list,
    "Subjects": subjects_autobio_list,
    "Languages": languages_autobio_list,
    "Key": keys_autobio_list
})

df_autobio.to_csv('1000 autobio books.csv', index=False)

print("autobio data saved to 'autobio_books.csv'")
