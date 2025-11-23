import requests
import json
import random

def scrapeEvents(lat=40.4406, lon=-79.9959, max_distance=50):
    events = []

    # Build API URL using coordinates (Pittsburgh default)
    url = f"https://www.volunteerconnector.org/api/search/?md={max_distance}&lat={lat}&lon={lon}&so=Proximity"

    print(f"Fetching from API: {url}")

    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error: API returned status {response.status_code}")
        return getSampleEvents()

    data = response.json()

    print(f"Found {data.get('count', 0)} opportunities")

    results = data.get('results', [])

    for i, item in enumerate(results):
        # Extract title
        title = item.get('title', f'Volunteer Event {i+1}')

        # Extract organization
        org = item.get('organization', {}).get('name', 'Local Organization')

        # Extract description (may contain HTML, strip it simply)
        desc = item.get('description', title)
        # Simple HTML tag removal
        desc = desc.replace('<p>', '').replace('</p>', ' ').replace('<br>', ' ')
        desc = desc.replace('<strong>', '').replace('</strong>', '')
        desc = desc[:100]  # Truncate

        # Extract dates/time
        dates_raw = item.get('dates', 'TBD')
        if 'Ongoing' in dates_raw:
            event_date = 'Ongoing'
            event_time = 'Flexible'
        else:
            event_date = dates_raw[:20] if len(dates_raw) > 20 else dates_raw
            event_time = 'See details'

        # Extract location from audience
        audience = item.get('audience', {})
        lat = audience.get('latitude')
        lon = audience.get('longitude')
        regions = audience.get('regions', [])

        if regions:
            event_location = regions[0][:20] if regions else 'Pittsburgh'
        else:
            event_location = 'Pittsburgh Area'

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
            'desc': desc[:50],
            'hours': random.randint(2, 5),
            'date': event_date,
            'time': event_time,
            'location': event_location[:20],
            'mapX': random.randint(100, 350),
            'mapY': random.randint(200, 450),
            'impact': random.randint(3, 5),
            'code': code
        }
        events.append(event)

    if len(events) == 0:
        print('No events found, using samples')
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
        }
    ]

def saveEvents(events):
    f = open('events.json', 'w')
    json.dump(events, f, indent=2)
    f.close()
    print(f"Saved {len(events)} events to events.json")

if __name__ == '__main__':
    print("Fetching volunteer events from API...")
    # Pittsburgh coordinates: 40.4406, -79.9959
    events = scrapeEvents(40.4406, -79.9959, 50)
    saveEvents(events)
    print("Done!")
