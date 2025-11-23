"""
Givr Model - Data Structures and Loading
No graphics in this file - pure data handling
"""

import json
import os

# ============================================================================
# EVENT DATA STRUCTURE
# ============================================================================

class Event:
    """Represents a volunteer event/opportunity"""

    def __init__(self, data):
        self.id = data.get('id', 0)
        self.title = data.get('title', '')
        self.organization = data.get('organization', '')
        self.category = data.get('category', '')
        self.description = data.get('description', '')
        self.hours = data.get('hours', 0)
        self.date = data.get('date', '')
        self.timeRange = data.get('timeRange', '')
        self.location = data.get('location', '')
        self.mapX = data.get('mapX', 0)
        self.mapY = data.get('mapY', 0)
        self.difficulty = data.get('difficulty', 1)  # 1-3
        self.impactLevel = data.get('impactLevel', 1)  # 1-5
        self.verificationCode = data.get('verificationCode', '')

    def toDict(self):
        """Convert event to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'organization': self.organization,
            'category': self.category,
            'description': self.description,
            'hours': self.hours,
            'date': self.date,
            'timeRange': self.timeRange,
            'location': self.location,
            'mapX': self.mapX,
            'mapY': self.mapY,
            'difficulty': self.difficulty,
            'impactLevel': self.impactLevel,
            'verificationCode': self.verificationCode
        }

    def isWeekend(self):
        """Check if event is on weekend"""
        return 'Sat' in self.date or 'Sun' in self.date

    def __repr__(self):
        return f"Event({self.id}: {self.title})"


# ============================================================================
# USER DATA STRUCTURE
# ============================================================================

class User:
    """Represents a user profile"""

    def __init__(self, username, password, name=''):
        self.username = username
        self.password = password
        self.name = name

        # Preferences
        self.selectedCategories = set()
        self.timePreference = None  # 'weekdays', 'weekends', 'either'
        self.experienceLevel = None  # 'new', 'experienced'

        # Progress
        self.savedEventIds = []
        self.completedEventIds = []
        self.verifiedEventIds = []

        # Stats
        self.totalPoints = 0
        self.totalHours = 0
        self.currentTier = 1
        self.weeklyStreak = 0

        # Badges
        self.unlockedBadges = set()
        self.badgeProgress = {}

    def toDict(self):
        """Convert user to dictionary for storage"""
        return {
            'username': self.username,
            'password': self.password,
            'name': self.name,
            'selectedCategories': list(self.selectedCategories),
            'timePreference': self.timePreference,
            'experienceLevel': self.experienceLevel,
            'savedEventIds': self.savedEventIds,
            'completedEventIds': self.completedEventIds,
            'verifiedEventIds': self.verifiedEventIds,
            'totalPoints': self.totalPoints,
            'totalHours': self.totalHours,
            'currentTier': self.currentTier,
            'weeklyStreak': self.weeklyStreak,
            'unlockedBadges': list(self.unlockedBadges),
            'badgeProgress': self.badgeProgress
        }

    @classmethod
    def fromDict(cls, data):
        """Create user from dictionary"""
        user = cls(data['username'], data['password'], data.get('name', ''))
        user.selectedCategories = set(data.get('selectedCategories', []))
        user.timePreference = data.get('timePreference')
        user.experienceLevel = data.get('experienceLevel')
        user.savedEventIds = data.get('savedEventIds', [])
        user.completedEventIds = data.get('completedEventIds', [])
        user.verifiedEventIds = data.get('verifiedEventIds', [])
        user.totalPoints = data.get('totalPoints', 0)
        user.totalHours = data.get('totalHours', 0)
        user.currentTier = data.get('currentTier', 1)
        user.weeklyStreak = data.get('weeklyStreak', 0)
        user.unlockedBadges = set(data.get('unlockedBadges', []))
        user.badgeProgress = data.get('badgeProgress', {})
        return user


# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def loadEvents(filepath='data/events.json'):
    """Load events from JSON file"""
    try:
        # Try relative path first
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                data = json.load(f)
                return [Event(e) for e in data]

        # Try from script directory
        scriptDir = os.path.dirname(os.path.abspath(__file__))
        fullPath = os.path.join(scriptDir, filepath)
        if os.path.exists(fullPath):
            with open(fullPath, 'r') as f:
                data = json.load(f)
                return [Event(e) for e in data]

        print(f"Warning: Could not find {filepath}, using sample data")
        return createSampleEvents()
    except Exception as e:
        print(f"Error loading events: {e}")
        return createSampleEvents()


def createSampleEvents():
    """Create sample events as fallback"""
    sampleData = [
        {
            'id': 1,
            'title': 'Park Cleanup Drive',
            'organization': 'Pittsburgh Parks Conservancy',
            'category': 'Environment',
            'description': 'Help beautify Schenley Park by picking up litter and planting flowers.',
            'hours': 3,
            'date': 'Sat, Nov 25',
            'timeRange': '10:00 AM - 1:00 PM',
            'location': 'Oakland',
            'mapX': 280,
            'mapY': 320,
            'difficulty': 2,
            'impactLevel': 3,
            'verificationCode': 'PARK'
        },
        {
            'id': 2,
            'title': 'Youth Tutoring Session',
            'organization': 'CMU Community Tutoring',
            'category': 'Education',
            'description': 'Tutor middle school students in math and science subjects.',
            'hours': 2,
            'date': 'Mon, Nov 27',
            'timeRange': '4:00 PM - 6:00 PM',
            'location': 'East Liberty',
            'mapX': 320,
            'mapY': 250,
            'difficulty': 3,
            'impactLevel': 4,
            'verificationCode': 'TUTR'
        },
        {
            'id': 3,
            'title': 'Food Bank Sorting',
            'organization': 'Greater Pittsburgh Food Bank',
            'category': 'Community',
            'description': 'Sort and package food donations for families in need.',
            'hours': 4,
            'date': 'Sun, Nov 26',
            'timeRange': '9:00 AM - 1:00 PM',
            'location': 'Downtown',
            'mapX': 150,
            'mapY': 400,
            'difficulty': 2,
            'impactLevel': 5,
            'verificationCode': 'FOOD'
        },
        {
            'id': 4,
            'title': 'Senior Center Visit',
            'organization': 'Friendship Senior Center',
            'category': 'Health',
            'description': 'Spend time with seniors playing games and sharing stories.',
            'hours': 2,
            'date': 'Wed, Nov 29',
            'timeRange': '2:00 PM - 4:00 PM',
            'location': 'Friendship',
            'mapX': 300,
            'mapY': 280,
            'difficulty': 1,
            'impactLevel': 4,
            'verificationCode': 'SNRS'
        },
        {
            'id': 5,
            'title': 'Art Workshop Assistant',
            'organization': 'Pittsburgh Arts Council',
            'category': 'Arts',
            'description': 'Help run a community painting workshop for all ages.',
            'hours': 3,
            'date': 'Sat, Dec 2',
            'timeRange': '1:00 PM - 4:00 PM',
            'location': 'Shadyside',
            'mapX': 340,
            'mapY': 300,
            'difficulty': 2,
            'impactLevel': 3,
            'verificationCode': 'ARTS'
        }
    ]
    return [Event(e) for e in sampleData]


# ============================================================================
# FILTERING AND SORTING
# ============================================================================

def filterEventsByCategory(events, categories):
    """Filter events by selected categories"""
    if not categories:
        return events
    return [e for e in events if e.category in categories]


def filterEventsByTime(events, timePreference):
    """Filter events by time preference"""
    if timePreference == 'either' or timePreference is None:
        return events
    elif timePreference == 'weekends':
        return [e for e in events if e.isWeekend()]
    elif timePreference == 'weekdays':
        return [e for e in events if not e.isWeekend()]
    return events


def sortEventsByImpact(events, descending=True):
    """Sort events by impact level"""
    return sorted(events, key=lambda e: e.impactLevel, reverse=descending)


def sortEventsByHours(events, descending=False):
    """Sort events by hours required"""
    return sorted(events, key=lambda e: e.hours, reverse=descending)


def getFilteredEvents(events, categories=None, timePreference=None, sortBy='impact'):
    """Get filtered and sorted events based on preferences"""
    result = events

    if categories:
        result = filterEventsByCategory(result, categories)

    if timePreference:
        result = filterEventsByTime(result, timePreference)

    if sortBy == 'impact':
        result = sortEventsByImpact(result)
    elif sortBy == 'hours':
        result = sortEventsByHours(result)

    return result


# ============================================================================
# TIER AND BADGE DEFINITIONS
# ============================================================================

TIERS = {
    1: {'name': 'New Giver', 'minPoints': 0},
    2: {'name': 'Community Builder', 'minPoints': 100},
    3: {'name': 'Impact Leader', 'minPoints': 300},
    4: {'name': 'Civic Champion', 'minPoints': 600}
}

CATEGORIES = ['Environment', 'Education', 'Community', 'Health', 'Arts']

CATEGORY_COLORS = {
    'Environment': (76, 175, 80),   # Green
    'Education': (33, 150, 243),    # Blue
    'Community': (255, 152, 0),     # Orange
    'Health': (244, 67, 54),        # Red
    'Arts': (156, 39, 176)          # Purple
}

BADGE_DEFINITIONS = {
    'getting_started': {
        'name': 'Getting Started',
        'description': 'Verify your first event',
        'icon': 'star'
    },
    'weekend_warrior': {
        'name': 'Weekend Warrior',
        'description': 'Verify 3+ weekend events',
        'target': 3
    },
    'green_guardian': {
        'name': 'Green Guardian',
        'description': 'Verify 5 environment events',
        'target': 5,
        'category': 'Environment'
    },
    'kids_champion': {
        'name': "Kids' Champion",
        'description': 'Verify 5 education events',
        'target': 5,
        'category': 'Education'
    },
    'marathon_volunteer': {
        'name': 'Marathon Volunteer',
        'description': 'Complete 20+ verified hours',
        'target': 20
    },
    'neighborhood_navigator': {
        'name': 'Neighborhood Navigator',
        'description': 'Events in 3+ distinct areas',
        'target': 3
    }
}
