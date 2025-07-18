import requests
from bs4 import BeautifulSoup
import time

def scrape_courses(n, delay, search_query):
    """
    Scrapes the first n courses matching the given search_query from the Stepik catalog via HTML.
    delay — pause between requests (in seconds) to avoid overloading the server.
    Returns a list of dictionaries with data for each course.
    """
    base_url = "https://stepik.org/catalog"
    courses = []
    page = 1

    while len(courses) < n:
        params = {
            "query": search_query,
            "page": page
        }
        resp = requests.get(base_url, params=params)
        print(resp.text[:1000])  # <-- inspect what actually is in the HTML
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        cards = soup.select(".course-card")  # course card containers

        if not cards:
            # no more courses on next page
            break

        for card in cards:
            if len(courses) >= n:
                break

            # Course title
            title_el = card.select_one(".course-card__title")
            title = title_el.get_text(strip=True) if title_el else "-"

            # Short description (subtitle)
            subtitle_el = card.select_one(".course-card__subtitle")
            subtitle = subtitle_el.get_text(strip=True) if subtitle_el else "-"

            # Link to the course page
            link_el = card.select_one("a.course-card-link")
            link = "https://stepik.org" + link_el["href"] if link_el and link_el.get("href") else "-"

            # Number of learners
            learners_el = card.select_one(".course-stats__value")
            learners = learners_el.get_text(strip=True) if learners_el else "-"

            # Course language (if available)
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

if __name__ == "__main__":
    # Example: scrape first 5 courses for 'java'
    first_n = scrape_courses(5, 0.5, 'java')
    for idx, course in enumerate(first_n, 1):
        print(f"{idx}. {course['title']}")
        print(f"   Language: {course['language']} | Learners: {course['learners']}")
        print(f"   Description: {course['subtitle']}")
        print(f"   Link: {course['link']}")
        print("-" * 50)
