# ============================================================================
# AI_givr - Intelligent Event Generation System
# Learns from user swipes to generate personalized volunteer events
# ============================================================================

import random

class UserPreferenceEngine:
    """
    Tracks user swipe behavior and learns preferences to generate
    personalized volunteer events - similar to Tinder's algorithm.
    """

    def __init__(self):
        # Track what the user likes/dislikes
        self.liked_events = []
        self.skipped_events = []

        # Learned preferences (weighted scores)
        self.category_scores = {
            'Environment': 0.0,
            'Education': 0.0,
            'Community': 0.0,
            'Health': 0.0,
            'Arts': 0.0
        }

        # Time preferences learned from swipes
        self.time_scores = {
            'morning': 0.0,    # Before 12PM
            'afternoon': 0.0,  # 12PM-5PM
            'evening': 0.0     # After 5PM
        }

        # Day preferences
        self.day_scores = {
            'weekday': 0.0,
            'weekend': 0.0
        }

        # Duration preferences (hours)
        self.preferred_duration = 3.0
        self.duration_tolerance = 2.0

        # Location preferences
        self.location_scores = {}

        # Impact level preference
        self.preferred_impact = 3.0

        # Keyword preferences extracted from liked events
        self.keyword_scores = {}

        # Track generation specificity - increases as user swipes more
        self.specificity_level = 1  # 1-5, increases with more swipes

    def record_swipe(self, event, liked):
        """
        Record a user's swipe decision and update preferences.
        liked=True for right swipe (save), liked=False for left swipe (skip)
        """
        weight = 1.0 if liked else -0.5  # Likes are weighted more than skips

        if liked:
            self.liked_events.append(event)
        else:
            self.skipped_events.append(event)

        # Update category preference
        category = event.get('category', '')
        if category in self.category_scores:
            self.category_scores[category] += weight

        # Update time preference
        time_str = event.get('time', '')
        time_period = self._parse_time_period(time_str)
        if time_period:
            self.time_scores[time_period] += weight

        # Update day preference
        date_str = event.get('date', '')
        day_type = self._parse_day_type(date_str)
        if day_type:
            self.day_scores[day_type] += weight

        # Update location preference
        location = event.get('location', '')
        if location:
            if location not in self.location_scores:
                self.location_scores[location] = 0.0
            self.location_scores[location] += weight

        # Update duration preference (moving average towards liked events)
        if liked:
            hours = event.get('hours', 3)
            self.preferred_duration = (self.preferred_duration * 0.7) + (hours * 0.3)

        # Update impact preference
        if liked:
            impact = event.get('impact', 3)
            self.preferred_impact = (self.preferred_impact * 0.7) + (impact * 0.3)

        # Extract and score keywords from title and description
        self._update_keywords(event, weight)

        # Update specificity level based on total swipes
        total_swipes = len(self.liked_events) + len(self.skipped_events)
        self.specificity_level = min(5, 1 + total_swipes // 3)

    def _parse_time_period(self, time_str):
        """Parse time string to determine morning/afternoon/evening"""
        time_str = time_str.upper()
        if 'AM' in time_str:
            # Check the starting hour
            try:
                hour = int(time_str.split('AM')[0].split('-')[0].strip())
                if hour < 12:
                    return 'morning'
            except:
                pass
        if 'PM' in time_str:
            try:
                parts = time_str.split('PM')[0].split('-')[0].strip()
                # Remove any AM part
                parts = parts.replace('AM', '').strip()
                hour = int(parts) if parts.isdigit() else 12
                if hour < 5 or hour == 12:
                    return 'afternoon'
                else:
                    return 'evening'
            except:
                return 'afternoon'
        return None

    def _parse_day_type(self, date_str):
        """Parse date string to determine weekday/weekend"""
        date_lower = date_str.lower()
        if 'sat' in date_lower or 'sun' in date_lower:
            return 'weekend'
        elif any(day in date_lower for day in ['mon', 'tue', 'wed', 'thu', 'fri']):
            return 'weekday'
        return None

    def _update_keywords(self, event, weight):
        """Extract and score keywords from event"""
        # Common volunteer-related keywords to track
        text = f"{event.get('title', '')} {event.get('desc', '')}".lower()

        keywords = [
            'cleanup', 'clean', 'park', 'trail', 'river', 'nature', 'tree', 'garden',
            'tutor', 'teach', 'mentor', 'student', 'school', 'homework', 'education',
            'food', 'meal', 'hunger', 'donate', 'bank', 'pantry', 'soup',
            'senior', 'elderly', 'visit', 'companion', 'care', 'health', 'hospital',
            'art', 'paint', 'music', 'creative', 'workshop', 'mural', 'craft',
            'build', 'construct', 'repair', 'habitat', 'house', 'shelter',
            'animal', 'pet', 'shelter', 'rescue', 'wildlife',
            'kids', 'children', 'youth', 'camp', 'play',
            'community', 'neighborhood', 'local', 'civic'
        ]

        for keyword in keywords:
            if keyword in text:
                if keyword not in self.keyword_scores:
                    self.keyword_scores[keyword] = 0.0
                self.keyword_scores[keyword] += weight

    def get_top_categories(self, n=2):
        """Get the user's top preferred categories"""
        sorted_cats = sorted(self.category_scores.items(), key=lambda x: x[1], reverse=True)
        return [cat for cat, score in sorted_cats[:n] if score > 0]

    def get_top_keywords(self, n=5):
        """Get the user's top preferred keywords"""
        sorted_kw = sorted(self.keyword_scores.items(), key=lambda x: x[1], reverse=True)
        return [kw for kw, score in sorted_kw[:n] if score > 0]

    def get_preferred_time(self):
        """Get the user's preferred time of day"""
        if not any(self.time_scores.values()):
            return None
        return max(self.time_scores.items(), key=lambda x: x[1])[0]

    def get_preferred_day(self):
        """Get the user's preferred day type"""
        if not any(self.day_scores.values()):
            return None
        return max(self.day_scores.items(), key=lambda x: x[1])[0]


class AIEventGenerator:
    """
    Generates new volunteer events based on learned user preferences.
    Events become more specific and tailored as the user swipes more.
    """

    def __init__(self, preference_engine):
        self.engine = preference_engine
        self.generated_event_id = 1000  # Start IDs at 1000 for generated events

        # Base templates for each category with increasing specificity
        self.event_templates = {
            'Environment': {
                1: [  # Level 1 - Generic
                    {'title': 'Park Volunteer Day', 'desc': 'Help maintain local parks'},
                    {'title': 'Nature Conservation', 'desc': 'Protect local wildlife'},
                    {'title': 'Green Initiative', 'desc': 'Environmental improvement project'},
                ],
                2: [  # Level 2 - More specific
                    {'title': 'Creek Cleanup Crew', 'desc': 'Remove trash from local waterways'},
                    {'title': 'Tree Planting Event', 'desc': 'Plant native trees in the community'},
                    {'title': 'Trail Maintenance', 'desc': 'Clear and maintain hiking trails'},
                    {'title': 'Recycling Education', 'desc': 'Teach recycling best practices'},
                ],
                3: [  # Level 3 - Specialized
                    {'title': 'Invasive Species Removal', 'desc': 'Remove harmful plants from natural areas'},
                    {'title': 'Bird Habitat Restoration', 'desc': 'Create nesting areas for local birds'},
                    {'title': 'Rain Garden Installation', 'desc': 'Build rain gardens to reduce runoff'},
                    {'title': 'Wildlife Monitoring', 'desc': 'Track and record local wildlife populations'},
                ],
                4: [  # Level 4 - Expert
                    {'title': 'Stream Ecosystem Survey', 'desc': 'Conduct water quality testing and species count'},
                    {'title': 'Native Pollinator Garden', 'desc': 'Design and plant gardens for bees and butterflies'},
                    {'title': 'Wetland Restoration Project', 'desc': 'Restore critical wetland habitats'},
                ],
                5: [  # Level 5 - Highly specialized
                    {'title': 'Urban Forest Inventory', 'desc': 'Map and catalog urban tree canopy'},
                    {'title': 'Climate Action Initiative', 'desc': 'Lead community carbon reduction efforts'},
                    {'title': 'Watershed Protection Lead', 'desc': 'Coordinate watershed conservation activities'},
                ]
            },
            'Education': {
                1: [
                    {'title': 'Tutoring Session', 'desc': 'Help students with schoolwork'},
                    {'title': 'Reading Buddy', 'desc': 'Read with young students'},
                    {'title': 'Homework Help', 'desc': 'Assist students after school'},
                ],
                2: [
                    {'title': 'Math Tutoring', 'desc': 'Help students with math concepts'},
                    {'title': 'Science Fair Mentor', 'desc': 'Guide students on science projects'},
                    {'title': 'ESL Conversation Partner', 'desc': 'Practice English with learners'},
                    {'title': 'College Prep Workshop', 'desc': 'Help students with applications'},
                ],
                3: [
                    {'title': 'STEM Workshop Leader', 'desc': 'Run hands-on science activities'},
                    {'title': 'Coding Club Mentor', 'desc': 'Teach programming basics to kids'},
                    {'title': 'Career Day Speaker', 'desc': 'Share your career experience'},
                    {'title': 'GED Tutoring', 'desc': 'Help adults earn their GED'},
                ],
                4: [
                    {'title': 'Robotics Team Coach', 'desc': 'Guide competitive robotics team'},
                    {'title': 'AP Course Tutor', 'desc': 'Help with advanced placement subjects'},
                    {'title': 'Financial Literacy Teacher', 'desc': 'Teach personal finance skills'},
                ],
                5: [
                    {'title': 'Curriculum Developer', 'desc': 'Create educational materials'},
                    {'title': 'STEM Program Coordinator', 'desc': 'Lead ongoing STEM initiatives'},
                    {'title': 'Educational Technology Trainer', 'desc': 'Train teachers on ed-tech tools'},
                ]
            },
            'Community': {
                1: [
                    {'title': 'Food Bank Helper', 'desc': 'Sort and distribute food donations'},
                    {'title': 'Community Event', 'desc': 'Help at local community events'},
                    {'title': 'Donation Drive', 'desc': 'Collect items for those in need'},
                ],
                2: [
                    {'title': 'Meal Delivery', 'desc': 'Deliver meals to homebound residents'},
                    {'title': 'Clothing Closet Volunteer', 'desc': 'Sort and organize donated clothing'},
                    {'title': 'Community Garden', 'desc': 'Grow food for the community'},
                    {'title': 'Neighborhood Beautification', 'desc': 'Clean and beautify public spaces'},
                ],
                3: [
                    {'title': 'Homeless Outreach', 'desc': 'Connect homeless individuals with resources'},
                    {'title': 'Refugee Welcome Team', 'desc': 'Help refugees settle in the community'},
                    {'title': 'Housing Assistance', 'desc': 'Help families find stable housing'},
                    {'title': 'Legal Aid Clinic Support', 'desc': 'Assist at free legal clinics'},
                ],
                4: [
                    {'title': 'Disaster Relief Coordinator', 'desc': 'Organize emergency response efforts'},
                    {'title': 'Affordable Housing Build', 'desc': 'Construct homes for families in need'},
                    {'title': 'Community Health Fair', 'desc': 'Organize health screening events'},
                ],
                5: [
                    {'title': 'Nonprofit Board Member', 'desc': 'Provide strategic leadership'},
                    {'title': 'Grant Writing Support', 'desc': 'Help organizations secure funding'},
                    {'title': 'Community Organizer', 'desc': 'Lead grassroots advocacy efforts'},
                ]
            },
            'Health': {
                1: [
                    {'title': 'Hospital Volunteer', 'desc': 'Assist staff and comfort patients'},
                    {'title': 'Senior Companion', 'desc': 'Spend time with elderly residents'},
                    {'title': 'Health Fair Helper', 'desc': 'Support community health events'},
                ],
                2: [
                    {'title': 'Wellness Workshop', 'desc': 'Lead fitness or nutrition classes'},
                    {'title': 'Blood Drive Support', 'desc': 'Help organize blood donation events'},
                    {'title': 'Mental Health Advocacy', 'desc': 'Raise awareness about mental health'},
                    {'title': 'Memory Care Activities', 'desc': 'Lead activities for dementia patients'},
                ],
                3: [
                    {'title': 'Hospice Companion', 'desc': 'Provide comfort to hospice patients'},
                    {'title': 'Therapy Dog Handler', 'desc': 'Bring therapy animals to facilities'},
                    {'title': 'Crisis Line Volunteer', 'desc': 'Provide phone support for those in crisis'},
                    {'title': 'Addiction Recovery Support', 'desc': 'Mentor those in recovery'},
                ],
                4: [
                    {'title': 'Medical Mission Prep', 'desc': 'Organize medical outreach supplies'},
                    {'title': 'Caregiver Respite', 'desc': 'Give caregivers a needed break'},
                    {'title': 'Patient Navigator', 'desc': 'Help patients navigate healthcare system'},
                ],
                5: [
                    {'title': 'Health Policy Advocate', 'desc': 'Advocate for healthcare access'},
                    {'title': 'Clinical Trial Outreach', 'desc': 'Connect patients with research opportunities'},
                    {'title': 'Public Health Campaign Lead', 'desc': 'Lead community health initiatives'},
                ]
            },
            'Arts': {
                1: [
                    {'title': 'Art Workshop Helper', 'desc': 'Assist with community art classes'},
                    {'title': 'Museum Volunteer', 'desc': 'Help at local museums'},
                    {'title': 'Performance Event Staff', 'desc': 'Support live performances'},
                ],
                2: [
                    {'title': 'Youth Art Instructor', 'desc': 'Teach art skills to children'},
                    {'title': 'Mural Painting Project', 'desc': 'Create public art installations'},
                    {'title': 'Theater Production Crew', 'desc': 'Help with stage productions'},
                    {'title': 'Music Program Volunteer', 'desc': 'Support community music education'},
                ],
                3: [
                    {'title': 'Art Therapy Assistant', 'desc': 'Use art to help healing'},
                    {'title': 'Cultural Festival Organizer', 'desc': 'Plan diverse cultural celebrations'},
                    {'title': 'Photography Mentor', 'desc': 'Teach photography to beginners'},
                    {'title': 'Dance Instruction', 'desc': 'Lead community dance classes'},
                ],
                4: [
                    {'title': 'Public Art Installation', 'desc': 'Design permanent community art'},
                    {'title': 'Film Festival Coordinator', 'desc': 'Organize local film screenings'},
                    {'title': 'Arts Grant Reviewer', 'desc': 'Review applications for arts funding'},
                ],
                5: [
                    {'title': 'Artist Residency Coordinator', 'desc': 'Manage artist-in-residence programs'},
                    {'title': 'Cultural Heritage Preservation', 'desc': 'Document and preserve local history'},
                    {'title': 'Creative Placemaking Lead', 'desc': 'Transform spaces through art'},
                ]
            }
        }

        # Pittsburgh neighborhoods for location generation
        self.neighborhoods = [
            'Oakland', 'Shadyside', 'Squirrel Hill', 'East Liberty', 'Lawrenceville',
            'Downtown', 'Strip District', 'North Shore', 'South Side', 'Bloomfield',
            'Highland Park', 'Point Breeze', 'Friendship', 'Garfield', 'Hill District',
            'Homewood', 'Regent Square', 'Greenfield', 'Hazelwood', 'Mt. Washington'
        ]

        # Organizations by category
        self.organizations = {
            'Environment': [
                'Pittsburgh Parks Conservancy', 'Western PA Conservancy',
                'TreePittsburgh', 'Nine Mile Run Watershed', 'Allegheny Land Trust',
                'Clean Water Action', 'Pittsburgh Botanic Garden'
            ],
            'Education': [
                'Pittsburgh Public Schools', 'Reading Is FUNdamental',
                'Literacy Pittsburgh', 'Carnegie Library', 'Remake Learning',
                "Boys & Girls Club", 'YMCA Pittsburgh'
            ],
            'Community': [
                'Greater Pittsburgh Food Bank', 'Light of Life Mission',
                'Habitat for Humanity', 'United Way', 'Community Human Services',
                'Pittsburgh Mercy', 'Neighborhood Allies'
            ],
            'Health': [
                'UPMC Community Outreach', 'Allegheny Health Network',
                'American Red Cross', 'PACE Senior Services',
                'Alzheimer\'s Association', 'NAMI Pittsburgh', 'Bethlehem Haven'
            ],
            'Arts': [
                'Pittsburgh Cultural Trust', 'Mattress Factory',
                'Assemble PGH', 'Pittsburgh Center for the Arts',
                'Sprout Fund', 'City of Asylum', 'Brew House Association'
            ]
        }

    def generate_events(self, count=3, existing_events=None):
        """
        Generate new personalized events based on learned preferences.
        Returns a list of new event dictionaries.
        """
        existing_events = existing_events or []
        existing_titles = {e['title'].lower() for e in existing_events}

        new_events = []
        attempts = 0
        max_attempts = count * 10  # Prevent infinite loops

        # Get preference data
        top_categories = self.engine.get_top_categories(3) or list(self.engine.category_scores.keys())
        preferred_time = self.engine.get_preferred_time()
        preferred_day = self.engine.get_preferred_day()
        specificity = self.engine.specificity_level

        # Weight categories based on preference scores
        category_weights = []
        for cat in top_categories:
            weight = max(1, self.engine.category_scores.get(cat, 0) + 1)
            category_weights.extend([cat] * int(weight * 2))

        # Add some variety - include less preferred categories occasionally
        all_categories = list(self.engine.category_scores.keys())
        category_weights.extend(all_categories)

        while len(new_events) < count and attempts < max_attempts:
            attempts += 1

            # Select category (weighted toward preferences)
            category = random.choice(category_weights)

            # Get template based on specificity level
            templates = self.event_templates[category].get(specificity,
                        self.event_templates[category][1])
            template = random.choice(templates)

            # Check for duplicate
            if template['title'].lower() in existing_titles:
                continue

            # Generate event details
            event = self._create_event_from_template(
                template, category, preferred_time, preferred_day
            )

            if event['title'].lower() not in existing_titles:
                new_events.append(event)
                existing_titles.add(event['title'].lower())

        return new_events

    def _create_event_from_template(self, template, category, preferred_time, preferred_day):
        """Create a full event from a template"""
        self.generated_event_id += 1

        # Generate time based on preference
        time_str = self._generate_time(preferred_time)

        # Generate date based on preference
        date_str = self._generate_date(preferred_day)

        # Calculate hours based on preference
        hours = max(1, min(6, round(self.engine.preferred_duration + random.uniform(-1, 1))))

        # Select organization
        org = random.choice(self.organizations[category])

        # Select location (prefer locations user has liked)
        location = self._select_location()

        # Calculate impact based on preference
        impact = max(1, min(5, round(self.engine.preferred_impact + random.uniform(-1, 1))))

        # Generate verification code
        code = template['title'][:4].upper().replace(' ', '') + str(random.randint(0, 9))

        # Enhance description based on specificity
        desc = self._enhance_description(template['desc'], category)

        # Map category to icon type
        category_icons = {
            'Environment': 'tree',
            'Education': 'book',
            'Community': 'box',
            'Health': 'heart',
            'Arts': 'palette'
        }
        icon = category_icons.get(category, 'star')

        return {
            'id': self.generated_event_id,
            'title': template['title'],
            'org': org,
            'category': category,
            'desc': desc,
            'hours': hours,
            'date': date_str,
            'time': time_str,
            'location': location,
            'mapX': random.randint(100, 350),
            'mapY': random.randint(200, 450),
            'impact': impact,
            'code': code,
            'icon': icon,  # Add icon based on category
            'ai_generated': True  # Flag to identify AI-generated events
        }

    def _generate_time(self, preferred_time):
        """Generate a time string based on preferences"""
        if preferred_time == 'morning':
            start_hours = [8, 9, 10]
        elif preferred_time == 'evening':
            start_hours = [5, 6, 7]
        else:  # afternoon or no preference
            start_hours = [12, 1, 2, 3]

        start = random.choice(start_hours)
        duration = max(1, min(4, round(self.engine.preferred_duration)))
        end = start + duration

        if start < 12:
            start_str = f"{start}AM"
        elif start == 12:
            start_str = "12PM"
        else:
            start_str = f"{start}PM" if start <= 12 else f"{start-12}PM"

        if end < 12:
            end_str = f"{end}AM"
        elif end == 12:
            end_str = "12PM"
        else:
            end_str = f"{end}PM" if end <= 12 else f"{end-12}PM"

        return f"{start_str}-{end_str}"

    def _generate_date(self, preferred_day):
        """Generate a date string based on preferences"""
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        months = ['Nov', 'Dec', 'Jan']

        if preferred_day == 'weekend':
            day = random.choice(['Sat', 'Sun'])
        elif preferred_day == 'weekday':
            day = random.choice(['Mon', 'Tue', 'Wed', 'Thu', 'Fri'])
        else:
            day = random.choice(days)

        month = random.choice(months)
        date_num = random.randint(1, 28)

        return f"{day}, {month} {date_num}"

    def _select_location(self):
        """Select location, weighted toward preferred locations"""
        if self.engine.location_scores:
            # Get top locations
            sorted_locs = sorted(self.engine.location_scores.items(),
                               key=lambda x: x[1], reverse=True)
            preferred_locs = [loc for loc, score in sorted_locs[:5] if score > 0]

            if preferred_locs and random.random() < 0.6:
                return random.choice(preferred_locs)

        return random.choice(self.neighborhoods)

    def _enhance_description(self, base_desc, category):
        """Enhance description based on user's keyword preferences"""
        top_keywords = self.engine.get_top_keywords(3)

        # Add specificity based on keywords
        enhancements = {
            'Environment': {
                'cleanup': 'Remove litter and debris',
                'park': 'in beautiful park settings',
                'trail': 'along scenic trails',
                'nature': 'connecting with nature',
                'tree': 'helping our urban forest grow',
            },
            'Education': {
                'tutor': 'providing one-on-one support',
                'mentor': 'guiding students toward success',
                'kids': 'working with enthusiastic young learners',
                'homework': 'helping students master concepts',
            },
            'Community': {
                'food': 'fighting hunger in our community',
                'donate': 'making a direct impact',
                'community': 'strengthening neighborhood bonds',
            },
            'Health': {
                'senior': 'bringing joy to older adults',
                'care': 'providing compassionate support',
                'health': 'promoting wellness',
            },
            'Arts': {
                'art': 'unleashing creativity',
                'paint': 'creating lasting beauty',
                'music': 'sharing the gift of music',
            }
        }

        cat_enhancements = enhancements.get(category, {})

        for keyword in top_keywords:
            if keyword in cat_enhancements:
                return f"{base_desc} - {cat_enhancements[keyword]}"

        return base_desc


# Global instance management
_preference_engine = None
_event_generator = None

def get_preference_engine():
    """Get or create the global preference engine"""
    global _preference_engine
    if _preference_engine is None:
        _preference_engine = UserPreferenceEngine()
    return _preference_engine

def get_event_generator():
    """Get or create the global event generator"""
    global _event_generator
    if _event_generator is None:
        _event_generator = AIEventGenerator(get_preference_engine())
    return _event_generator

def reset_ai_system():
    """Reset the AI system (for new users)"""
    global _preference_engine, _event_generator
    _preference_engine = UserPreferenceEngine()
    _event_generator = AIEventGenerator(_preference_engine)


# ============================================================================
# Public API - Use these functions from givr_app
# ============================================================================

def record_swipe(event, liked):
    """
    Record a user's swipe decision.
    Call this when user swipes right (liked=True) or left (liked=False)
    """
    engine = get_preference_engine()
    engine.record_swipe(event, liked)

def generate_new_events(existing_events, count=3):
    """
    Generate new personalized events based on user's swipe history.
    Returns a list of new event dictionaries.
    """
    generator = get_event_generator()
    return generator.generate_events(count, existing_events)

def should_generate_more_events(current_index, total_events, threshold=2):
    """
    Check if we should generate more events.
    Returns True when user is running low on events to swipe.
    """
    remaining = total_events - current_index
    return remaining <= threshold

def get_preference_summary():
    """
    Get a summary of the user's learned preferences.
    Useful for debugging or showing user their profile.
    """
    engine = get_preference_engine()
    return {
        'top_categories': engine.get_top_categories(3),
        'preferred_time': engine.get_preferred_time(),
        'preferred_day': engine.get_preferred_day(),
        'preferred_duration': round(engine.preferred_duration, 1),
        'preferred_impact': round(engine.preferred_impact, 1),
        'top_keywords': engine.get_top_keywords(5),
        'specificity_level': engine.specificity_level,
        'total_likes': len(engine.liked_events),
        'total_skips': len(engine.skipped_events)
    }

def get_specificity_level():
    """Get the current specificity level (1-5)"""
    return get_preference_engine().specificity_level
