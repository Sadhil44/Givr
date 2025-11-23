from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import random
import time

def scrapeEvents(location='Pittsburgh, PA'):
    events = []

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run without opening browser
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Set up driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = f"https://engage.pointsoflight.org/search?loc={location.replace(' ', '%20').replace(',', '%2C')}"

    print(f"Loading {url}...")
    driver.get(url)

    # Wait for page to load (Points of Light uses dynamic loading)
    time.sleep(8)

    # Get page source and parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find all opportunity cards - Points of Light uses <li> elements with shadow class
    listings = soup.find_all('li', class_='bg-white')

    print(f"Found {len(listings)} listings")

    for i, listing in enumerate(listings[:10]):
        # Extract title from h3 element
        title_elem = listing.find('h3')
        if title_elem:
            title = title_elem.get_text(strip=True)
        else:
            title = f"Volunteer Event {i+1}"

        # Extract organization from p with text-md class
        org_elem = listing.find('p', class_='text-gray-700')
        if org_elem:
            org = org_elem.get_text(strip=True)
        else:
            org = "Local Organization"

        # Extract location from the first p with text-gray-500
        location_elems = listing.find_all('p', class_='text-gray-500')
        event_location = "Pittsburgh"
        for elem in location_elems:
            text = elem.get_text(strip=True)
            if 'PA' in text or 'Pittsburgh' in text:
                event_location = text.replace(',', '').strip()
                break

        # Use title as description base
        desc = title[:50] if len(title) > 50 else title

        # Assign category based on keywords
        category = assignCategory(title + ' ' + desc)

        # Generate verification code
        code = ''.join(c for c in title.upper() if c.isalpha())[:4]
        if len(code) < 4:
            code = code + 'X' * (4 - len(code))

        event = {
            'id': i + 100,
            'title': title[:30],
            'org': org[:30],
            'category': category,
            'desc': desc,
            'hours': random.randint(2, 5),
            'date': f"Dec {random.randint(1, 28)}",
            'time': random.choice(['9AM-12PM', '10AM-1PM', '1PM-4PM', '2PM-5PM']),
            'location': event_location[:20],
            'mapX': random.randint(100, 350),
            'mapY': random.randint(200, 450),
            'impact': random.randint(3, 5),
            'code': code
        }
        events.append(event)

    driver.quit()

    # If no events found, return samples
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
        },
        {
            'id': 101, 'title': 'Food Bank Sorting',
            'org': 'Greater PGH Food Bank', 'category': 'Community',
            'desc': 'Sort and package food donations',
            'hours': 4, 'date': 'Sun, Dec 8', 'time': '10AM-2PM',
            'location': 'Duquesne', 'mapX': 120, 'mapY': 400,
            'impact': 5, 'code': 'FOOD'
        },
        {
            'id': 102, 'title': 'Youth Tutoring',
            'org': 'Pittsburgh Literacy', 'category': 'Education',
            'desc': 'Tutor K-8 students in reading/math',
            'hours': 2, 'date': 'Mon, Dec 9', 'time': '4PM-6PM',
            'location': 'East Liberty', 'mapX': 320, 'mapY': 250,
            'impact': 4, 'code': 'YOUT'
        },
        {
            'id': 103, 'title': 'Senior Companion',
            'org': 'UPMC Senior Services', 'category': 'Health',
            'desc': 'Visit and chat with elderly residents',
            'hours': 2, 'date': 'Tue, Dec 10', 'time': '1PM-3PM',
            'location': 'Shadyside', 'mapX': 340, 'mapY': 300,
            'impact': 4, 'code': 'SENI'
        },
        {
            'id': 104, 'title': 'Mural Painting',
            'org': 'Sprout Fund', 'category': 'Arts',
            'desc': 'Help paint community mural',
            'hours': 5, 'date': 'Sat, Dec 14', 'time': '10AM-3PM',
            'location': 'Lawrenceville', 'mapX': 250, 'mapY': 220,
            'impact': 4, 'code': 'MURA'
        },
        {
            'id': 105, 'title': 'River Trail Maintenance',
            'org': 'Friends of the Riverfront', 'category': 'Environment',
            'desc': 'Clear brush and repair trail signs',
            'hours': 4, 'date': 'Sun, Dec 15', 'time': '8AM-12PM',
            'location': 'North Shore', 'mapX': 120, 'mapY': 280,
            'impact': 4, 'code': 'RIVE'
        },
        {
            'id': 106, 'title': 'Homework Help',
            'org': 'Boys & Girls Club', 'category': 'Education',
            'desc': 'Help kids with after-school homework',
            'hours': 2, 'date': 'Wed, Dec 11', 'time': '3:30PM-5:30PM',
            'location': 'Hill District', 'mapX': 180, 'mapY': 350,
            'impact': 4, 'code': 'HOME'
        },
        {
            'id': 107, 'title': 'Meal Delivery',
            'org': 'Meals on Wheels', 'category': 'Community',
            'desc': 'Deliver meals to homebound seniors',
            'hours': 3, 'date': 'Thu, Dec 12', 'time': '11AM-2PM',
            'location': 'Squirrel Hill', 'mapX': 300, 'mapY': 350,
            'impact': 5, 'code': 'MEAL'
        },
        {
            'id': 108, 'title': 'Animal Shelter Helper',
            'org': 'Humane Animal Rescue', 'category': 'Community',
            'desc': 'Walk dogs and socialize cats',
            'hours': 3, 'date': 'Sat, Dec 14', 'time': '1PM-4PM',
            'location': 'East End', 'mapX': 310, 'mapY': 280,
            'impact': 3, 'code': 'ANIM'
        },
        {
            'id': 109, 'title': 'Museum Guide',
            'org': 'Carnegie Museum', 'category': 'Arts',
            'desc': 'Guide visitors through exhibits',
            'hours': 4, 'date': 'Sun, Dec 15', 'time': '12PM-4PM',
            'location': 'Oakland', 'mapX': 280, 'mapY': 320,
            'impact': 3, 'code': 'MUSE'
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