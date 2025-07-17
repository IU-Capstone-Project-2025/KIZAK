import requests
from bs4 import BeautifulSoup
import time
import schedule
import threading
import json


def scrape_courses(n, delay, search_query):
    base_url = "https://stepik.org/catalog"
    courses = []
    page = 1

    while len(courses) < n:
        params = {
            "query": search_query,
            "page": page
        }
        resp = requests.get(base_url, params=params)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        cards = soup.select(".course-card")

        if not cards:
            break

        for card in cards:
            if len(courses) >= n:
                break

            title_el = card.select_one(".course-card__title")
            title = title_el.get_text(strip=True) if title_el else "-"

            subtitle_el = card.select_one(".course-card__subtitle")
            subtitle = subtitle_el.get_text(strip=True) if subtitle_el else "-"

            link_el = card.select_one("a.course-card-link")
            link = "https://stepik.org" + link_el["href"] if link_el and link_el.get("href") else "-"

            learners_el = card.select_one(".course-stats__value")
            learners = learners_el.get_text(strip=True) if learners_el else "-"

            lang_el = card.select_one(".course-meta__language")
            language = lang_el.get_text(strip=True) if lang_el else "-"

            courses.append({
                "title": title,
                "subtitle": subtitle,
                "link": link,
                "learners": learners,
                "language": language
            })

        page += 1
        time.sleep(delay)

    return courses


def send_to_endpoint(courses, endpoint_url):
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(endpoint_url, headers=headers, data=json.dumps(courses))
        response.raise_for_status()
        print("Successfully sent courses to the endpoint.")
    except requests.RequestException as e:
        print(f"Failed to send data: {e}")


def job():
    print("Running weekly scraping job...")
    courses = scrape_courses(10, 1, 'java')  # Customize as needed
    send_to_endpoint(courses, "http://back:8000/update_courses/")


def run_scheduler():
    schedule.every().monday.at("10:00").do(job)

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    # Run scheduler in a background thread so it doesn't block the main thread
    t = threading.Thread(target=run_scheduler, daemon=True)
    t.start()
    print("Course scraper service is running. Press Ctrl+C to exit.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping course scraper service.")
