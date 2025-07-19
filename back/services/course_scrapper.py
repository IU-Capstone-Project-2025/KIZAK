from utils.logger import logger
from db.resource import create_resource
from models.resource import ResourceCreate, ResourceSend, ResourceLevel
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import asyncio
import re
import aiohttp  # Replaced requests with aiohttp for async HTTP calls


class CourseraScraper():
    async def scrape_course(self, course_url):
        logger.info(f"Scraping course: {course_url}")
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(course_url, wait_until="networkidle")

            await page.wait_for_selector("h1[data-e2e='hero-title']", timeout=10000)
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(0.5)
            
            html = await page.content()
            await browser.close()
        
        logger.info(f"Course HTML content retrieved successfully.")
        soup = BeautifulSoup(html, "html.parser")

        description = None
        description_div = soup.find("div", class_="rc-TogglableContent about-section collapsed")
        if description_div:
            content_inner = description_div.find("div", class_="content-inner")
            if content_inner:
                description = content_inner.get_text(strip=True)
        
        skills = []
        about_section = soup.find("div", id="about")
        if about_section:
            skills_ul = about_section.find("ul", class_="css-yk0mzy")
            if skills_ul:
                skill_links = skills_ul.find_all("a")
                skills = [link.get_text(strip=True) for link in skill_links if link.get_text(strip=True)]

        difficulty = None
        duration = None
        metadata = soup.find("p", class_="css-vac8rf", string=re.compile("Начинающий|Средний|Продвинутый"))
        if metadata:
            metadata_text = metadata.get_text(strip=True)
            if "Начинающий" in metadata_text:
                difficulty = "Beginner"
            elif "Средний" in metadata_text:
                difficulty = "Intermediate"
            elif "Продвинутый" in metadata_text:
                difficulty = "Advanced"
            
            duration_match = re.search(r"(\d+\s*–\s*\d+\s*месяц|\d+\s*месяц|\d+\s*–\s*\d+\s*недел|\d+\s*недел|\d+\s*час)", metadata_text)
            duration = duration_match.group(0) if duration_match else None
        
        return {
            "description": description,
            "skills": skills,
            "difficulty": difficulty if difficulty is not None else 'Beginner',
            "duration": duration
        }

    async def scrape_courses(self, query):
        params = {"query": query}
        url = f"https://www.coursera.org/search?{urlencode(params)}"
        logger.info(f"Search URL: {url}")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(url, wait_until="networkidle")
            await page.wait_for_selector("a[href^='/learn/']")

            try:
                await page.click("div[role='button'][aria-haspopup='listbox']")
                await page.wait_for_selector("ul[role='listbox']", timeout=5000)
                try:
                    await page.click("li[role='option'] >> text='Newest'", timeout=2000)
                except:
                    await page.click("li[role='option'] >> text='Самые новые'", timeout=2000)
                await page.wait_for_selector("a[href^='/learn/']:not(.loading)")
                await asyncio.sleep(5)
            except Exception as e:
                logger.error(f"Could not sort by newest: {e}")

            html = await page.content()
            await browser.close()
        
        logger.info(f"Search completed successfully.")
        soup = BeautifulSoup(html, "html.parser")
        courses = []
        
        course_cards = soup.find_all("div", class_="cds-ProductCard-gridCard")
        logger.info(f"Found {len(course_cards)} course cards.")
        
        for index, card in enumerate(course_cards):
            logger.info(f"Processing course card {index + 1}/{len(course_cards)}")
            link = card.find("a", class_="cds-CommonCard-titleLink")
            if not link or not link.get("href"):
                continue
                
            full_url = f"https://www.coursera.org{link['href']}"
            
            title_elem = card.find("h3", class_="cds-CommonCard-title")
            title = title_elem.get_text(strip=True) if title_elem else None
            
            author_elem = card.find("p", class_="cds-ProductCard-partnerNames")
            author = author_elem.get_text(strip=True) if author_elem else None
            
            rating_elem = card.find("span", class_="css-6ecy9b")
            rating = rating_elem.get_text(strip=True) if rating_elem else 0
            
            reviews_elem = card.find("div", class_="css-vac8rf", string=re.compile("Рецензии:"))
            reviews = 0
            if reviews_elem:
                reviews_text = reviews_elem.get_text(strip=True)
                reviews = re.search(r"(\d+[\s,]?\d*)", reviews_text.replace(" ", ""))
                reviews = reviews.group(1) if reviews else 0
            
            course_data = {
                "url": full_url,
                "title": title,
                "author": author,
                "rating": rating if rating is not None else 5,
                "reviews_count": reviews,
                "difficulty_level": None,
                "duration": None,
                "description": None,
                "skills": [],
                "source": "coursera"
            }
            
            try:
                detailed_info = await self.scrape_course(full_url)
                course_data.update(detailed_info)
            except Exception as e:
                logger.error(f"Failed to scrape detailed info for {full_url}: {str(e)}")
            
            courses.append(course_data)

        return courses


class Scraper():
    def __init__(self):
        self.queries = ['python']
        self.coursera = CourseraScraper()

    async def scrape_courses(self):
        self.results = []
        for query in self.queries:
            logger.info(f"Scraping courses for query: {query}")
            courses = await self.coursera.scrape_courses(query)
            self.results.extend(courses)
        return self.results

    async def add_to_db(self):
        async with aiohttp.ClientSession() as session:
            for course in self.results:
                try:
                    skills = course.get('skills', [])
                    if skills is None:
                        continue
                    title = course.get('title')
                    description = course.get('description')
                    url = course.get('url')
                    level = course.get('difficulty_level', 'Beginner')
                    if level is None:
                        level = 'Beginner'
                    platform = course.get('source', 'coursera')
                    rating = float(course.get('rating', 0)) if course.get('rating') is not None else None

                    created_resource = await create_resource(
                        ResourceCreate(
                            resource_type='Course',
                            title=title,
                            summary=description,
                            content=url,
                            level=ResourceLevel(level),
                            price=0.0,
                            language='English',
                            platform=platform,
                            rating=rating,
                            skills_covered=skills,
                            certificate_available=True
                        )
                    )
                    
                    # Async HTTP request
                    async with session.post(
                        "http://ml:8001/courses/",
                        json={
                            "resource_id": str(created_resource.resource_id),
                            "title": title,
                            "description": description,
                            "skills": skills  
                        }
                    ) as response:
                        if response.status != 200:
                            logger.error(f"Failed to send course to ML service: {await response.text()}")

                except Exception as e:
                    logger.error(f"Error adding course {course.get('title')} to DB: {e}")
                    continue
