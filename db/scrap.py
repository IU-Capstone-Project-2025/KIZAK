import requests
from bs4 import BeautifulSoup

def scrape_coursera_course(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("h1").get_text(strip=True) if soup.find("h1") else "N/A"

    author = soup.find(class_="cds-119 cds-113 cds-115 css-1uwt8wn cds-142").find("span").text

    students = int(soup.find("div", class_="css-1qi3xup").find("span").find("span").text.replace(",", ""))

    rating = float(soup.find("div", class_="cds-119 cds-Typography-base css-h1jogs cds-121")["aria-label"].split(" ")[0])

    difficulty = soup.find_all("div", class_="css-fk6qfz")[1].text.split(" ")[0]

    skills_data = soup.find_all("a", class_="cds-119 cds-113 cds-115 css-113xph7 cds-142")

    skills = [i.text for i in skills_data]

    description = soup.find("div", class_="cds-9 css-0 cds-11 cds-grid-item cds-56 cds-79 cds-94").text

    time_to_pass = soup.find_all("div", class_="css-fw9ih3")

    for i, idx in enumerate(time_to_pass):
        print(idx, i)

    return {
        "title": title,
        "author": author,
        "students": students,
        "rating": rating,
        "difficulty": difficulty,
        "skills": skills,
        "description": description,
        "time_to_pass": time_to_pass,
        "price": None,
        "source": "Coursera"
    }

if __name__ == "__main__":
    url = "https://www.coursera.org/learn/python-for-applied-data-science-ai"
    data = scrape_coursera_course(url)
    print(data)