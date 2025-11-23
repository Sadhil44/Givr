from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import random
import time

def scrapeEvents(location='Pittsburgh, PA'):
    events = []

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Set up driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = f"https://engage.pointsoflight.org/search?loc={location.replace(' ', '%20').replace(',', '%2C')}"

    print(f"Loading {url}...")
    driver.get(url)

    # Wait for page to load
    time.sleep(8)

    # Get page source and parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find all opportunity cards
    listings = soup.find_all('li', class_='bg-white')

    print(f"Found {len(listings)} listings")

    for i, listing in enumerate(listings):
        # Extract title from h3 element
        title_elem = listing.find('h3')
        if title_elem:
            title = title_elem.get_text(strip=True)
        else:
            title = f"Volunteer Event {i+1}"

        # Extract organization from p with text-gray-700 class
        org_elem = listing.find('p', class_='text-gray-700')
        if org_elem:
            org = org_elem.get_text(strip=True)
        else:
            org = "Local Organization"

        # Extract location and date/time from p elements with text-gray-500
        gray_elems = listing.find_all('p', class_='text-gray-500')
        event_location = "Pittsburgh"
        event_date = "TBD"
        event_time = "TBD"

        for elem in gray_elems:
            text = elem.get_text(strip=True)
            if 'PA' in text or 'Pittsburgh' in text:
                event_location = text.replace(',', '').strip()
            elif any(month in text for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']):
                parts = text.split()
                if len(parts) >= 2:
                    event_date = parts[0] + ' ' + parts[1]
                    if len(parts) >= 3:
                        event_time = ' '.join(parts[2:])
                    else:
                        event_time = "See details"
            elif 'Recruiting' in text:
                event_date = "Ongoing"
                event_time = "Flexible"

        # Use title as description base
        desc = title

        # Assign category based on keywords
        category = assignCategory(title + ' ' + desc)

        # Generate verification code
        code = ''.join(c for c in title.upper() if c.isalpha())[:4]
        if len(code) < 4:
            code = code + 'X' * (4 - len(code))

        # Smart truncation at word boundaries
        short_title = truncate_at_word(title, 20)
        short_org = truncate_at_word(org, 20)
        short_desc = truncate_at_word(desc, 35)
        short_location = truncate_at_word(event_location, 15)

        event = {
            'id': i + 100,
            'title': short_title,
            'fullTitle': title[:50],
            'org': short_org,
            'fullOrg': org[:40],
            'category': category,
            'desc': short_desc,
            'fullDesc': title[:100],
            'hours': random.randint(2, 5),
            'date': event_date,
            'time': event_time,
            'location': event_location[:15],
            'fullLocation': event_location[:30],
            'mapX': random.randint(100, 350),
            'mapY': random.randint(200, 450),
            'impact': random.randint(3, 5),
            'code': code
        }
        events.append(event)

    driver.quit()

    if len(events) == 0:
        print('No events scraped, using samples')
        events = getSampleEvents()

    return events

def assignCategory(text):
    text = text.lower()
    if 'environment' in text or 'park' in text or 'clean' in text or 'garden' in text:
        return 'Environment'
    elif 'tutor' in text or 'teach' in text or 'school' in text or 'education' in text:
        return 'Education'
    elif 'health' in text or 'hospital' in text or 'senior' in text:
        return 'Health'
    elif 'art' in text or 'music' in text or 'museum' in text:
        return 'Arts'
    else:
        return 'Community'

def getSampleEvents():
    return [
        {
            'id': 100, 'title': 'Schenley Park Cleanup',
            'org': 'Pittsburgh Parks', 'category': 'Environment',
            'desc': 'Help clean trails and pick up litter',
            'hours': 3, 'date': 'Sat, Dec 7', 'time': '9AM-12PM',
            'location': 'Oakland', 'mapX': 280, 'mapY': 320,
            'impact': 4, 'code': 'SCHE'
        }
    ]

def saveEvents(events):
    f = open('events.json', 'w')
    json.dump(events, f, indent=2)
    f.close()
    print(f"Saved {len(events)} events to events.json")

if __name__ == '__main__':
    print("Scraping volunteer events...")
    events = scrapeEvents()
    saveEvents(events)
    print("Done!")
