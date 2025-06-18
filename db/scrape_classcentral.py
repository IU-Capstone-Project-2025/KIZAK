import requests
from bs4 import BeautifulSoup
import json
import re
import os
from datetime import datetime

BASE_URL = "https://www.classcentral.com"

def debug_print_jsonld(soup, max_chars=500):
    # In debug mode, print JSON-LD snippets from the page
    scripts = soup.find_all("script", type="application/ld+json")
    for i, script in enumerate(scripts):
        text = script.string or ""
        preview = text.strip().replace("\n", " ")[:max_chars]
        print(f"[JSON-LD #{i}] {preview}...")

def inspect_detail_selectors(html, keywords=("rating", "hours", "week", "Language", "Syllabus")):
    """
    For debugging: find strings containing given keywords and print their parent tag and a snippet.
    """
    soup = BeautifulSoup(html, "html.parser")
    for kw in keywords:
        print(f"--- Searching for keyword '{kw}' ---")
        for el in soup.find_all(string=re.compile(kw, re.IGNORECASE)):
            parent = el.parent
            classes = parent.get("class")
            snippet = str(parent)[:300].replace("\n", " ")
            print(f"Text: '{el.strip()}'  Tag: <{parent.name} class={classes}> snippet: {snippet}...")
        print()

def fetch_course_details(course_url, debug=False):
    """
    Given a Class Central course page URL, extract:
    - rating: average rating (string or None)
    - num_reviews: number of reviews (string or None)
    - language: course language (string or None)
    - duration: duration info (string or None)
    - syllabus: list of topics, each as dict with keys 'title' and 'details' (list or None)
    """
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        resp = requests.get(course_url, headers=headers, timeout=10)
    except Exception as e:
        if debug:
            print(f"Request error for {course_url}: {e}")
        return {"rating": None, "num_reviews": None, "language": None, "duration": None, "syllabus": None}

    if resp.status_code != 200:
        if debug:
            print(f"Request error {course_url}: status {resp.status_code}")
        return {"rating": None, "num_reviews": None, "language": None, "duration": None, "syllabus": None}

    html = resp.text
    soup = BeautifulSoup(html, "html.parser")

    if debug:
        print(f"\n=== Debug for {course_url} ===")
        inspect_detail_selectors(html)
        print("=== JSON-LD content ===")
        debug_print_jsonld(soup)
        print("=========================")

    rating = num_reviews = language = duration = None
    syllabus = []

    # 1) Parse JSON-LD
    for script in soup.find_all("script", type="application/ld+json"):
        if not script.string:
            continue
        try:
            data = json.loads(script.string)
        except Exception:
            text = script.string.strip()
            start = text.find('{')
            if start != -1:
                try:
                    data = json.loads(text[start:])
                except:
                    continue
        def rec(o):
            nonlocal rating, num_reviews, language, duration
            if isinstance(o, dict):
                t = o.get("@type", "")
                if t in ("Course", "Product", "CreativeWork"):
                    agg = o.get("aggregateRating") or {}
                    rv = agg.get("ratingValue") or agg.get("ratingCount")
                    rc = agg.get("reviewCount") or agg.get("ratingCount")
                    if rv and not rating:
                        rating = str(rv)
                    if rc and not num_reviews:
                        num_reviews = str(rc)
                    lang = o.get("inLanguage") or o.get("courseLanguage")
                    if lang and not language:
                        language = ", ".join(lang) if isinstance(lang, list) else str(lang)
                    tr = o.get("timeRequired")
                    if tr and not duration:
                        duration = str(tr)
                for v in o.values():
                    rec(v)
            elif isinstance(o, list):
                for i in o:
                    rec(i)
        rec(data)
    if debug:
        print("After JSON-LD parsing:", dict(rating=rating, num_reviews=num_reviews,
                                             language=language, duration=duration))

    # 2) From HTML if JSON-LD missing rating/reviews
    if not (rating and num_reviews):
        tag = soup.find("span", attrs={"aria-label": re.compile(r"out of", re.I)})
        if tag:
            m = re.search(r"(\d+\.?\d*)", tag.get("aria-label", ""))
            if m:
                rating = rating or m.group(1)
        if tag and tag.parent:
            m2 = re.search(r"based on\s*(\d+[,\d]*)", tag.parent.get_text(" ", strip=True), re.I)
            if m2:
                num_reviews = num_reviews or m2.group(1).replace(",", "")
        if not (rating and num_reviews):
            for t in soup.find_all(string=re.compile(r"rating", re.I)):
                txt = t.strip()
                m = re.search(r"(\d+\.?\d*)\s*rating", txt, re.I)
                if m and not rating:
                    rating = m.group(1)
                m2 = re.search(r"based on\s*(\d+[,\d]*)", txt, re.I)
                if m2 and not num_reviews:
                    num_reviews = m2.group(1).replace(",", "")
                if rating and num_reviews:
                    break
        if debug:
            print("After HTML parsing for rating:", dict(rating=rating, num_reviews=num_reviews))

    # 3) Language from Course Details section if still missing
    if not language:
        cd = soup.select_one("section[data-test='course-info'], section.course-details")
        if cd:
            for li in cd.find_all("li"):
                txt = li.get_text(" ", strip=True)
                if txt.lower().startswith("language"):
                    parts = txt.split(":", 1)
                    if len(parts) == 2 and re.match(r"^[A-Za-z ]+$", parts[1].strip()):
                        language = parts[1].strip()
                    break
        if debug:
            print("After HTML parsing for language:", dict(language=language))

    # 4) Duration from HTML if still missing
    if not duration:
        wd = soup.select_one("div[data-test='workload'], div.course-duration")
        if wd:
            duration = wd.get_text(" ", strip=True)
        else:
            m = re.search(r"(\d+\s*(?:hours?|weeks?|months?))", html, re.I)
            if m:
                duration = m.group(1).strip()
        if debug:
            print("After HTML parsing for duration:", dict(duration=duration))

    # 5) Syllabus / Curriculum
    header = None
    for tag in soup.find_all(['h2', 'h3']):
        txt = tag.get_text(strip=True).lower()
        if "syllabus" in txt or "curriculum" in txt or "what you'll learn" in txt:
            header = tag
            break
    if header:
        section = header.find_parent("section")
        ul = section.find("ul") if section else None
        if not ul:
            ul = header.find_next("ul")
        if ul:
            for li in ul.find_all("li", recursive=False):
                sub = li.find("ul", recursive=False)
                if not sub:
                    title = li.get_text(" ", strip=True)
                    details = None
                else:
                    title_parts = []
                    for x in li.contents:
                        if x is sub:
                            continue
                        text = str(x).strip()
                        if text:
                            title_parts.append(text)
                    title = " ".join(title_parts).strip()
                    details = [s.get_text(" ", strip=True) for s in sub.find_all("li")]
                syllabus.append({"title": title, "details": details})
    if debug:
        print("Collected syllabus:", syllabus or None)

    return {
        "rating": rating,
        "num_reviews": num_reviews,
        "language": language,
        "duration": duration,
        "syllabus": syllabus or None
    }

def fetch_classcentral_html(save_path="classcentral_search.html", debug=False):
    """
    Fetch HTML for a Class Central search for 'python' and optionally save it locally.
    """
    url = f"{BASE_URL}/search?q=python"
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    except Exception as e:
        if debug:
            print(f"Search request error: {e}")
        return None

    if resp.status_code != 200:
        if debug:
            print("Search request returned status:", resp.status_code)
        return None

    html = resp.text
    if save_path:
        try:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(html)
        except Exception as e:
            if debug:
                print(f"Failed to save search HTML to {save_path}: {e}")
    return html

def parse_classcentral_courses(html=None, debug=False, limit=5):
    """
    Parse Class Central search results HTML to extract top courses:
    - title
    - url
    Then fetch details for each.
    """
    if html is None:
        html = fetch_classcentral_html(debug=debug)
        if not html:
            return []
    soup = BeautifulSoup(html, "html.parser")
    courses = []
    # Selector may change over time; adjust if needed
    for h2 in soup.select("h2.text-1.weight-semi")[:limit]:
        title = h2.get_text(strip=True)
        a = h2.find_parent("a", href=True)
        url = BASE_URL + a["href"] if a and a["href"].startswith("/course") else None
        details = fetch_course_details(url, debug=debug) if url else {
            "rating": None, "num_reviews": None, "language": None, "duration": None, "syllabus": None
        }
        entry = {
            "title": title,
            "url": url,
            **details
        }
        courses.append(entry)
    return courses

if __name__ == "__main__":
    # Directory to store results
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)

    debug_mode = False  # set True if you want verbose debug output

    # Collect top 5 courses
    courses = parse_classcentral_courses(debug=debug_mode, limit=5)

    # Generate filename with timestamp to avoid overwriting
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(results_dir, f"classcentral_courses_{ts}.json")

    # Save to JSON
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(courses, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(courses)} courses to {output_path}")
    except Exception as e:
        print(f"Error saving JSON: {e}")
