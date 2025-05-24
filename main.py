from curl_cffi import requests
from bs4 import BeautifulSoup
import logging
import csv
import time


def setup_request():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    
    return headers


def scrape_reviews(soup):
    reviews = []
    review_cards = soup.find_all(
        'div', attrs={'data-automation': 'reviewCard'})

    for review in review_cards:
        review_data = {
            'rating': '',
            'title': '',
            'text': '',
            'date': ''
        }

        rating_element = review.find('svg', class_='UctUV')
        if rating_element:
            review_data['rating'] = rating_element.find(
                'title').text.strip().replace(' of 5 bubbles', '')



        text_element = review.find(
            'span',class_='JguWG')
        if text_element:
            review_data['text'] = text_element.text.strip()


        reviews.append(review_data)
        time.sleep(3)

    return reviews


def generate_url(base_url, page_number):
    if page_number == 1:
        return base_url
    offset = (page_number - 1) * 10
    # Split the URL at 'Reviews' and insert the offset
    parts = base_url.split('Reviews')
    return f"{parts[0]}Reviews-or{offset}{parts[1]}"


def save_to_csv(reviews, filename, mode='w'):
    with open(filename, mode=mode, newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write header only if it's a new file
        if mode == 'w':
            header = ['RATING', 'REVIEW_TEXT']
            writer.writerow(header)

        # Write reviews with restaurant info
        for review in reviews:
            row = [
                review['rating'],
                review['text'],
            ]
            writer.writerow(row)


def main():
    base_url = 'https://www.tripadvisor.com/Attraction_Review-g189400-d735521-Reviews-Acropolis_Museum-Athens_Attica.html'
    headers = setup_request()
    output_filename = 'tripadvisor_acropilis_museum.csv'
    current_page = 1
    max_retries = 3
    last_page = 2309


    try:
        while True:
            url = generate_url(base_url, current_page)
            print(f"Scraping page {current_page}...")

            retries = 0
            while retries < max_retries:
                try:
                    response = requests.get(
                        url, headers=headers, 
                        impersonate="chrome110"
                        )
                    response.raise_for_status()
                    break
                except:
                    retries += 1
                    if retries == max_retries:
                        logging.error(
                            f"Failed to fetch page {current_page} after {max_retries} attempts:")
                        return
                    print(f"Retry {retries} for page {current_page}")
                    time.sleep(10)

            soup = BeautifulSoup(response.content, 'html.parser')
    
            print(f"Total pages to scrape: {last_page}")

            reviews = scrape_reviews(soup)

            # Save to CSV (append mode for all pages after the first)
            save_mode = 'w' if current_page == 1 else 'a'
            save_to_csv(reviews, output_filename, mode=save_mode)

            print(f"Page {current_page} completed.")

            if last_page and current_page >= last_page:
                print("Reached the last page. Scraping completed.")
                break

            current_page += 1
            time.sleep(10)  # Wait between pages

        print(f"All information saved successfully to {output_filename}")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
