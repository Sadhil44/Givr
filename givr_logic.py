"""
Givr Logic - App State, Rewards, and Game Logic
No cmu_graphics imports allowed in this file.
"""

from givr_model import loadEvents, filterEvents, sortEventsByPreference, ALL_CATEGORIES

# ============ APP STATE ============

class AppState:
    """Central state container for the Givr app."""

    def __init__(self):
        # Mode/screen navigation
        self.mode = 'intro'  # intro, preferences, swipe, allEvents, saved, map, rewards, eventDetail

        # User preferences
        self.selectedCategories = set()  # Set of category strings
        self.timePreference = 'either'  # weekday, weekend, either

        # Events data
        self.allEvents = []
        self.swipeDeck = []  # Events to swipe through
        self.currentCardIndex = 0
        self.savedEvents = []

        # Currently viewed event (for detail screen)
        self.detailEvent = None

        # Rewards/progress
        self.totalPoints = 0
        self.totalVerifiedHours = 0
        self.weeklyStreak = 0
        self.unlockedBadges = set()
        self.currentTier = 1

        # Swipe animation state
        self.cardOffsetX = 0
        self.cardOffsetY = 0
        self.isDragging = False
        self.dragStartX = 0
        self.dragStartY = 0

        # Verification dialog state
        self.showVerifyDialog = False
        self.verifyingEvent = None
        self.verifyCodeInput = ''
        self.verifyError = ''

        # Map filter
        self.mapShowSavedOnly = False

        # All events filter
        self.allEventsFilterCategory = None

    def loadAllEvents(self):
        """Load events from JSON file."""
        self.allEvents = loadEvents()

    def buildSwipeDeck(self):
        """
        Build the swipe deck based on user preferences.
        Excludes already-saved events.
        """
        # Get categories list (or None for all)
        cats = list(self.selectedCategories) if self.selectedCategories else None
        timeFilter = self.timePreference if self.timePreference != 'either' else None

        filtered = filterEvents(self.allEvents, cats, timeFilter)

        # Exclude saved events
        savedIds = {e.id for e in self.savedEvents}
        filtered = [e for e in filtered if e.id not in savedIds]

        # Sort by preference
        self.swipeDeck = sortEventsByPreference(filtered, cats)
        self.currentCardIndex = 0

    def getCurrentCard(self):
        """Get the current card to display."""
        if 0 <= self.currentCardIndex < len(self.swipeDeck):
            return self.swipeDeck[self.currentCardIndex]
        return None

    def swipeRight(self):
        """Save the current event and move to next."""
        card = self.getCurrentCard()
        if card:
            card.saved = True
            if card not in self.savedEvents:
                self.savedEvents.append(card)
            self.currentCardIndex += 1
        self.resetCardPosition()

    def swipeLeft(self):
        """Skip the current event and move to next."""
        self.currentCardIndex += 1
        self.resetCardPosition()

    def resetCardPosition(self):
        """Reset card offset for animation."""
        self.cardOffsetX = 0
        self.cardOffsetY = 0
        self.isDragging = False

    def saveEvent(self, event):
        """Save an event (from all events or detail view)."""
        event.saved = True
        if event not in self.savedEvents:
            self.savedEvents.append(event)

    def unsaveEvent(self, event):
        """Remove an event from saved."""
        event.saved = False
        if event in self.savedEvents:
            self.savedEvents.remove(event)

    def markCompleted(self, event):
        """Mark an event as completed (unverified)."""
        event.completed = True

    def verifyEvent(self, event, code):
        """
        Attempt to verify an event with the given code.
        Returns True if successful, False otherwise.
        """
        if code.upper() == event.verificationCode.upper():
            event.verified = True
            self._processVerification(event)
            return True
        return False

    def _processVerification(self, event):
        """Process rewards when an event is verified."""
        # Calculate points
        points = calculatePoints(event.hours, event.difficulty, event.impactLevel)
        self.totalPoints += points
        self.totalVerifiedHours += event.hours

        # Update streak (simplified - just increment for demo)
        self.weeklyStreak += 1

        # Check and unlock badges
        self._checkBadges(event)

        # Update tier
        self._updateTier()

    def _checkBadges(self, event):
        """Check and unlock any new badges."""
        badges = checkBadges(self)

        # Category-specific badges
        if event.category == 'Environment':
            envCount = sum(1 for e in self.savedEvents if e.verified and e.category == 'Environment')
            if envCount >= 5:
                badges.add('Green Guardian')
        if event.category == 'Education & Youth':
            eduCount = sum(1 for e in self.savedEvents if e.verified and e.category == 'Education & Youth')
            if eduCount >= 5:
                badges.add("Kids' Champion")

        self.unlockedBadges = badges

    def _updateTier(self):
        """Update user tier based on points."""
        self.currentTier = getTier(self.totalPoints)


# ============ REWARDS CALCULATIONS ============

def calculatePoints(hours, difficulty, impactLevel):
    """
    Calculate impact points for an event.
    Formula: base_points * difficulty_multiplier * impact_multiplier
    """
    basePoints = hours * 10
    diffMultiplier = 1 + (difficulty - 1) * 0.25  # 1.0, 1.25, 1.5
    impactMultiplier = 1 + (impactLevel - 1) * 0.2  # 1.0, 1.2, 1.4, 1.6, 1.8
    return int(basePoints * diffMultiplier * impactMultiplier)

def getTier(totalPoints):
    """
    Determine user tier based on total points.
    Tier 1: 0-99 points
    Tier 2: 100-299 points
    Tier 3: 300-599 points
    Tier 4: 600+ points
    """
    if totalPoints >= 600:
        return 4
    elif totalPoints >= 300:
        return 3
    elif totalPoints >= 100:
        return 2
    else:
        return 1

def getTierName(tier):
    """Get the display name for a tier."""
    names = {
        1: "New Giver",
        2: "Community Builder",
        3: "Impact Leader",
        4: "Civic Champion"
    }
    return names.get(tier, "New Giver")

def getPointsForNextTier(currentTier):
    """Get points needed to reach the next tier."""
    thresholds = {1: 100, 2: 300, 3: 600, 4: float('inf')}
    return thresholds.get(currentTier, 100)

def checkBadges(state):
    """
    Check which badges should be unlocked based on current state.
    Returns a set of badge names.
    """
    badges = set(state.unlockedBadges)

    # Count verified events
    verifiedEvents = [e for e in state.savedEvents if e.verified]
    verifiedCount = len(verifiedEvents)

    # Getting Started - first verified event
    if verifiedCount >= 1:
        badges.add('Getting Started')

    # Weekend Warrior - 3+ weekend events
    weekendCount = sum(1 for e in verifiedEvents if e.dayType == 'weekend')
    if weekendCount >= 3:
        badges.add('Weekend Warrior')

    # Marathon Volunteer - 20+ hours
    if state.totalVerifiedHours >= 20:
        badges.add('Marathon Volunteer')

    # Neighborhood Navigator - 3+ distinct areas
    locations = set(e.locationName for e in verifiedEvents)
    if len(locations) >= 3:
        badges.add('Neighborhood Navigator')

    return badges

# All possible badges
ALL_BADGES = [
    'Getting Started',
    'Weekend Warrior',
    'Green Guardian',
    "Kids' Champion",
    'Marathon Volunteer',
    'Neighborhood Navigator'
]

# Badge descriptions
BADGE_DESCRIPTIONS = {
    'Getting Started': 'Verify your first event',
    'Weekend Warrior': 'Verify 3+ weekend events',
    'Green Guardian': 'Verify 5 environment events',
    "Kids' Champion": 'Verify 5 education events',
    'Marathon Volunteer': '20+ verified hours',
    'Neighborhood Navigator': 'Events in 3+ areas'
}
