"""
Givr Model - Data Structures and Loading
No cmu_graphics imports allowed in this file.
"""

import json
import os

class Event:
    """Represents a volunteer event/opportunity."""

    def __init__(self, data):
        self.id = data.get('id', 0)
        self.title = data.get('title', '')
        self.organization = data.get('organization', '')
        self.description = data.get('description', '')
        self.category = data.get('category', '')
        self.hours = data.get('hours', 0)
        self.date = data.get('date', '')
        self.timeRange = data.get('timeRange', '')
        self.dayType = data.get('dayType', 'weekend')
        self.locationName = data.get('locationName', '')
        self.mapX = data.get('mapX', 200)
        self.mapY = data.get('mapY', 200)
        self.difficulty = data.get('difficulty', 1)
        self.impactLevel = data.get('impactLevel', 1)
        self.verificationCode = data.get('verificationCode', '0000')

        # User-specific state
        self.saved = False
        self.completed = False
        self.verified = False

    def getStatusText(self):
        if self.verified:
            return "Verified"
        elif self.completed:
            return "Completed (unverified)"
        else:
            return "Not completed"

def loadEvents():
    """Load events from the JSON file."""
    dataPath = os.path.join(os.path.dirname(__file__), 'data', 'events.json')
    try:
        with open(dataPath, 'r', encoding='utf-8') as f:
            rawData = json.load(f)
        return [Event(e) for e in rawData]
    except FileNotFoundError:
        print(f"Warning: Could not find {dataPath}")
        return []
    except json.JSONDecodeError:
        print(f"Warning: Could not parse {dataPath}")
        return []

def filterEvents(events, categories=None, dayType=None):
    """
    Filter events by category and day type.
    categories: list of category strings or None for all
    dayType: 'weekday', 'weekend', or None for either
    """
    result = []
    for event in events:
        # Category filter
        if categories and event.category not in categories:
            continue
        # Day type filter
        if dayType and dayType != 'either' and event.dayType != dayType:
            continue
        result.append(event)
    return result

def sortEventsByPreference(events, preferredCategories):
    """
    Sort events so preferred categories come first.
    """
    def priority(event):
        if preferredCategories and event.category in preferredCategories:
            return 0
        return 1
    return sorted(events, key=priority)

# Category colors for UI
CATEGORY_COLORS = {
    'Environment': 'forestGreen',
    'Education & Youth': 'royalBlue',
    'Community & Neighborhood': 'orange',
    'Health & Wellness': 'crimson',
    'Arts & Culture': 'purple'
}

# All available categories
ALL_CATEGORIES = [
    'Environment',
    'Education & Youth',
    'Community & Neighborhood',
    'Health & Wellness',
    'Arts & Culture'
]

# Time preferences
TIME_PREFERENCES = ['weekday', 'weekend', 'either']
