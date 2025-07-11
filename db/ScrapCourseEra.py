from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://www.coursera.org"

# Chrome WebDriver configuration
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service("/usr/bin/chromedriver")

def get_driver():
    """Initialize and return a headless Chrome WebDriver."""
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_window_size(1920, 1080)
    return driver

def scroll_until_no_change(driver, pause=2, max_scrolls=20):
    """
    Scroll down the page incrementally until no new content loads or max_scrolls is reached.
    """
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def parse_course_page(driver, url):
    """
    Extract course details from the given URL using the driver.
    Returns a dict with title, url, estimated_time, and topics.
    """
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Course title
    title_tag = soup.find("h1")
    title = title_tag.text.strip() if title_tag else "N/A"

    # Estimated duration
    duration = "N/A"
    for element in soup.find_all(['span', 'div']):
        text = element.get_text(strip=True).lower()
        if any(keyword in text for keyword in ['hour', 'week', 'month']):
            duration = element.get_text(strip=True)
            break

    # Course topics/skills
    topics = []
    skill_header = soup.find(lambda tag: tag.name in ['h2', 'h3', 'span'] and 'skill' in tag.text.lower())
    if skill_header:
        ul = skill_header.find_next('ul')
        if ul:
            topics = [li.text.strip() for li in ul.find_all('li')]

    return {
        "title": title,
        "url": url,
        "estimated_time": duration,
        "topics": topics
    }

def fetch_recent_courses(max_courses=30):
    """
    Fetch a list of recent courses from Coursera.
    Scrolls the search results page to load content, collects course URLs,
    and parses each course page up to max_courses.
    Returns a list of course info dicts.
    """
    driver = get_driver()
    driver.get(f"{BASE_URL}/search?sort=recent&page=1")
    time.sleep(3)
    scroll_until_no_change(driver)

    # Parse the search results page to collect course links
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    link_tags = soup.select(
        'a[href^="/learn/"], '
        'a[href^="/specializations/"], '
        'a[href^="/professional-certificates/"]'
    )
    urls = []
    for a in link_tags:
        href = a.get('href').split('?')[0]
        full_url = BASE_URL + href
        if full_url not in urls:
            urls.append(full_url)
    print(f"Found {len(urls)} courses")

    # Parse each course page
    results = []
    for url in urls[:max_courses]:
        try:
            info = parse_course_page(driver, url)
            results.append(info)
            print("Added course:", info['title'])
        except Exception as e:
            print(f"Error parsing {url}: {e}")

    driver.quit()
    return results

if __name__ == '__main__':
    courses = fetch_recent_courses()
    print(json.dumps(courses, indent=2, ensure_ascii=False))
