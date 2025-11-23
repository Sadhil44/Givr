import requests
import json
import random
import math
import urllib3

# Disable SSL warnings (needed for some systems)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def scrapeEvents(city='Pittsburgh', state='PA', lat=40.4406, lon=-79.9959, radius_km=50):
    events = []

    # Download from Volunteer.gov API
    print("Fetching from Volunteer.gov API...")

    # Try multiple possible endpoints
    urls_to_try = [
        f"https://www.volunteer.gov/s/sfsites/aura?r=1&other.VolunteerOpportunitySearch.getOpportunities=1",
        "https://www.volunteer.gov/s/volunteer-opportunities.json",
        "https://www.volunteer.gov/api/opportunities"
    ]

    data = None
    for url in urls_to_try:
        try:
            print(f"Trying: {url[:60]}...")
            response = requests.get(url, verify=False, timeout=10)
            if response.status_code == 200:
                data = response.json()
                print("Success!")
                break
        except:
            continue

    if not data:
        print("Could not fetch from Volunteer.gov API")
        print("Using sample events instead")
        return getSampleEvents()

    # Handle different response structures
    if isinstance(data, list):
        opportunities = data
    elif isinstance(data, dict):
        opportunities = data.get('opportunities', data.get('records', data.get('results', [])))
    else:
        opportunities = []

    print(f"Total opportunities in database: {len(opportunities)}")

    # Filter opportunities by location
    filtered = []

    for opp in opportunities:
        # Try different field names for location
        opp_city = opp.get('city', opp.get('City', ''))
        opp_state = opp.get('state', opp.get('State', opp.get('stateProvince', '')))
        opp_lat = opp.get('latitude', opp.get('Latitude', opp.get('lat', None)))
        opp_lon = opp.get('longitude', opp.get('Longitude', opp.get('lon', opp.get('lng', None))))

        # Check if it matches city/state
        city_match = city.lower() in opp_city.lower() if opp_city else False
        state_match = state.lower() == opp_state.lower() if opp_state else False

        # Check if within radius (if coordinates available)
        radius_match = False
        if opp_lat and opp_lon:
            try:
                distance = haversine_distance(lat, lon, float(opp_lat), float(opp_lon))
                radius_match = distance <= radius_km
            except:
                pass

        # Include if city/state match OR within radius
        if (city_match and state_match) or radius_match:
            filtered.append(opp)

    print(f"Found {len(filtered)} opportunities near {city}, {state}")

    # Process filtered opportunities
    for i, opp in enumerate(filtered[:100]):  # Limit to 100 events
        # Extract title
        title = opp.get('title', opp.get('Title', opp.get('positionTitle', f'Volunteer Event {i+1}')))

        # Extract organization/agency
        org = opp.get('agency', opp.get('Agency', opp.get('organization', 'Federal Agency')))

        # Extract description
        desc = opp.get('description', opp.get('Description', opp.get('duties', title)))
        desc = desc[:100] if desc else title

        # Extract dates
        start_date = opp.get('startDate', opp.get('StartDate', ''))
        end_date = opp.get('endDate', opp.get('EndDate', ''))

        if start_date:
            event_date = start_date[:10]  # Just date portion
            event_time = 'See details'
        else:
            event_date = 'Ongoing'
            event_time = 'Flexible'

        # Extract location
        site_name = opp.get('siteName', opp.get('locationName', opp.get('parkName', '')))
        opp_city = opp.get('city', opp.get('City', city))
        opp_state = opp.get('state', opp.get('State', state))

        if site_name:
            event_location = f"{site_name}"[:20]
        else:
            event_location = f"{opp_city}, {opp_state}"[:20]

        # Assign category
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
            'location': event_location,
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

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in km"""
    R = 6371  # Earth's radius in km

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c

def assignCategory(text):
    text = text.lower()
    if 'environment' in text or 'park' in text or 'clean' in text or 'garden' in text or 'trail' in text or 'forest' in text:
        return 'Environment'
    elif 'tutor' in text or 'teach' in text or 'school' in text or 'education' in text:
        return 'Education'
    elif 'health' in text or 'hospital' in text or 'senior' in text:
        return 'Health'
    elif 'art' in text or 'music' in text or 'museum' in text or 'historic' in text:
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
    print("Fetching volunteer events from Volunteer.gov...")
    # Pittsburgh with 50km radius
    events = scrapeEvents('Pittsburgh', 'PA', 40.4406, -79.9959, 50)
    saveEvents(events)
    print("Done!")
