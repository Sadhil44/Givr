from cmu_graphics import *
import math

# ============================================================================
# GIVR - Swipe to Give Back
# Complete UI/UX Implementation using cmu_graphics
# ============================================================================

def onAppStart(app):
    # App dimensions
    app.width = 400
    app.height = 700

    # ========== NAVIGATION STATE ==========
    app.mode = 'intro'  # intro, login, signup, preferences, swipe, allEvents, saved, map, rewards, eventDetail, verification, profile
    app.previousMode = None

    # ========== USER STATE ==========
    app.isLoggedIn = False
    app.currentUser = None
    app.users = {}  # username -> {password, name, preferences, stats}

    # Login/Signup form state
    app.loginUsername = ''
    app.loginPassword = ''
    app.signupUsername = ''
    app.signupPassword = ''
    app.signupName = ''
    app.activeField = None  # 'username', 'password', 'name'
    app.loginError = ''
    app.signupError = ''

    # ========== PREFERENCES STATE ==========
    app.categories = ['Environment', 'Education', 'Community', 'Health', 'Arts']
    app.categoryColors = {
        'Environment': rgb(76, 175, 80),
        'Education': rgb(33, 150, 243),
        'Community': rgb(255, 152, 0),
        'Health': rgb(244, 67, 54),
        'Arts': rgb(156, 39, 176)
    }
    app.selectedCategories = set()
    app.timePreference = None  # 'weekdays', 'weekends', 'either'
    app.experienceLevel = None  # 'new', 'experienced'

    # ========== EVENTS DATA ==========
    app.events = createSampleEvents()
    app.currentEventIndex = 0
    app.savedEvents = []
    app.completedEvents = []  # Events marked as completed
    app.verifiedEvents = []   # Events with verified codes

    # ========== SWIPE STATE ==========
    app.isDragging = False
    app.dragStartX = 0
    app.dragStartY = 0
    app.cardOffsetX = 0
    app.cardOffsetY = 0
    app.swipeThreshold = 100

    # ========== EVENT DETAIL STATE ==========
    app.selectedEvent = None
    app.detailSource = None  # 'swipe', 'allEvents', 'saved', 'map'

    # ========== VERIFICATION STATE ==========
    app.verificationEvent = None
    app.verificationCode = ''
    app.verificationError = ''

    # ========== MAP STATE ==========
    app.mapFilter = 'all'  # 'all' or 'saved'
    app.hoveredPin = None

    # ========== REWARDS STATE ==========
    app.totalPoints = 0
    app.totalHours = 0
    app.currentTier = 1
    app.tiers = {
        1: {'name': 'New Giver', 'minPoints': 0, 'color': rgb(158, 158, 158)},
        2: {'name': 'Community Builder', 'minPoints': 100, 'color': rgb(205, 127, 50)},
        3: {'name': 'Impact Leader', 'minPoints': 300, 'color': rgb(192, 192, 192)},
        4: {'name': 'Civic Champion', 'minPoints': 600, 'color': rgb(255, 215, 0)}
    }
    app.badges = createBadges()
    app.weeklyStreak = 0

    # ========== UI COLORS ==========
    app.bgColor = rgb(245, 245, 250)
    app.primaryColor = rgb(99, 102, 241)  # Indigo
    app.secondaryColor = rgb(139, 92, 246)  # Purple
    app.accentColor = rgb(236, 72, 153)  # Pink
    app.textColor = rgb(30, 30, 30)
    app.lightText = rgb(120, 120, 120)
    app.cardBg = rgb(255, 255, 255)
    app.successColor = rgb(34, 197, 94)
    app.errorColor = rgb(239, 68, 68)

    # ========== NAV BAR ==========
    app.navItems = ['Swipe', 'Events', 'Saved', 'Map', 'Rewards']
    app.navIcons = ['swipe', 'list', 'heart', 'map', 'star']

    # ========== SCROLL STATE ==========
    app.scrollY = 0
    app.maxScrollY = 0

def createSampleEvents():
    """Create sample volunteer events data"""
    return [
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
        },
        {
            'id': 6,
            'title': 'River Trail Restoration',
            'organization': 'Three Rivers Heritage Trail',
            'category': 'Environment',
            'description': 'Help restore and maintain the riverfront walking trails.',
            'hours': 4,
            'date': 'Sat, Dec 9',
            'timeRange': '8:00 AM - 12:00 PM',
            'location': 'North Shore',
            'mapX': 120,
            'mapY': 280,
            'difficulty': 3,
            'impactLevel': 4,
            'verificationCode': 'RIVR'
        },
        {
            'id': 7,
            'title': 'Homework Help Program',
            'organization': 'Boys & Girls Club',
            'category': 'Education',
            'description': 'Assist children with their homework after school.',
            'hours': 2,
            'date': 'Tue, Nov 28',
            'timeRange': '3:30 PM - 5:30 PM',
            'location': 'Hill District',
            'mapX': 180,
            'mapY': 350,
            'difficulty': 2,
            'impactLevel': 4,
            'verificationCode': 'HMWK'
        },
        {
            'id': 8,
            'title': 'Neighborhood Mural Project',
            'organization': 'Sprout Fund',
            'category': 'Arts',
            'description': 'Help paint a community mural celebrating local history.',
            'hours': 5,
            'date': 'Sun, Dec 3',
            'timeRange': '10:00 AM - 3:00 PM',
            'location': 'Lawrenceville',
            'mapX': 250,
            'mapY': 220,
            'difficulty': 2,
            'impactLevel': 4,
            'verificationCode': 'MURL'
        },
        {
            'id': 9,
            'title': 'Health Fair Support',
            'organization': 'UPMC Community Health',
            'category': 'Health',
            'description': 'Help set up and run health screening stations.',
            'hours': 4,
            'date': 'Sat, Dec 16',
            'timeRange': '9:00 AM - 1:00 PM',
            'location': 'South Side',
            'mapX': 160,
            'mapY': 450,
            'difficulty': 2,
            'impactLevel': 5,
            'verificationCode': 'HLTH'
        },
        {
            'id': 10,
            'title': 'Community Garden Day',
            'organization': 'Grow Pittsburgh',
            'category': 'Environment',
            'description': 'Help prepare community gardens for winter season.',
            'hours': 3,
            'date': 'Sun, Dec 10',
            'timeRange': '11:00 AM - 2:00 PM',
            'location': 'Bloomfield',
            'mapX': 290,
            'mapY': 260,
            'difficulty': 2,
            'impactLevel': 3,
            'verificationCode': 'GRDN'
        }
    ]

def createBadges():
    """Create badge definitions"""
    return {
        'getting_started': {
            'name': 'Getting Started',
            'description': 'Verify your first event',
            'icon': 'star',
            'unlocked': False,
            'color': rgb(255, 193, 7)
        },
        'weekend_warrior': {
            'name': 'Weekend Warrior',
            'description': 'Verify 3+ weekend events',
            'icon': 'sun',
            'unlocked': False,
            'color': rgb(255, 152, 0),
            'progress': 0,
            'target': 3
        },
        'green_guardian': {
            'name': 'Green Guardian',
            'description': 'Verify 5 environment events',
            'icon': 'leaf',
            'unlocked': False,
            'color': rgb(76, 175, 80),
            'progress': 0,
            'target': 5
        },
        'kids_champion': {
            'name': "Kids' Champion",
            'description': 'Verify 5 education events',
            'icon': 'book',
            'unlocked': False,
            'color': rgb(33, 150, 243),
            'progress': 0,
            'target': 5
        },
        'marathon_volunteer': {
            'name': 'Marathon Volunteer',
            'description': 'Complete 20+ verified hours',
            'icon': 'clock',
            'unlocked': False,
            'color': rgb(156, 39, 176),
            'progress': 0,
            'target': 20
        },
        'neighborhood_navigator': {
            'name': 'Neighborhood Navigator',
            'description': 'Events in 3+ distinct areas',
            'icon': 'map',
            'unlocked': False,
            'color': rgb(0, 188, 212),
            'progress': 0,
            'target': 3
        }
    }

# ============================================================================
# DRAWING FUNCTIONS
# ============================================================================

def redrawAll(app):
    # Background
    drawRect(0, 0, app.width, app.height, fill=app.bgColor)

    if app.mode == 'intro':
        drawIntroScreen(app)
    elif app.mode == 'login':
        drawLoginScreen(app)
    elif app.mode == 'signup':
        drawSignupScreen(app)
    elif app.mode == 'preferences':
        drawPreferencesScreen(app)
    elif app.mode == 'swipe':
        drawSwipeScreen(app)
    elif app.mode == 'allEvents':
        drawAllEventsScreen(app)
    elif app.mode == 'saved':
        drawSavedScreen(app)
    elif app.mode == 'map':
        drawMapScreen(app)
    elif app.mode == 'rewards':
        drawRewardsScreen(app)
    elif app.mode == 'eventDetail':
        drawEventDetailScreen(app)
    elif app.mode == 'verification':
        drawVerificationScreen(app)
    elif app.mode == 'profile':
        drawProfileScreen(app)

def drawIntroScreen(app):
    """Draw the intro/splash screen"""
    # Gradient background effect
    for i in range(app.height):
        ratio = i / app.height
        r = int(99 + (139 - 99) * ratio)
        g = int(102 + (92 - 102) * ratio)
        b = int(241 + (246 - 241) * ratio)
        drawLine(0, i, app.width, i, fill=rgb(r, g, b))

    # Logo circle
    drawCircle(app.width/2, 220, 80, fill=rgb(230, 230, 245), border=None)
    drawCircle(app.width/2, 220, 60, fill='white')

    # Heart icon in logo
    drawHeart(app.width/2, 220, 30, app.primaryColor)

    # App name
    drawLabel('Givr', app.width/2, 340, size=48, bold=True, fill='white')

    # Tagline
    drawLabel('Swipe to give back.', app.width/2, 390, size=18, fill='white')

    # Description
    drawLabel('Discover volunteer opportunities', app.width/2, 450, size=14, fill=rgb(220, 220, 240))
    drawLabel('that match your interests.', app.width/2, 470, size=14, fill=rgb(220, 220, 240))

    # Get Started button
    drawRoundedButton(app.width/2 - 120, 530, 240, 50, 'Get Started', 'white', app.primaryColor, 25)

    # Login link
    drawLabel('Already have an account? Log in', app.width/2, 610, size=14, fill=rgb(220, 220, 240))

def drawLoginScreen(app):
    """Draw the login screen"""
    # Header
    drawRect(0, 0, app.width, 120, fill=app.primaryColor)
    drawLabel('Welcome Back', app.width/2, 70, size=28, bold=True, fill='white')

    # Back button
    drawLabel('<', 30, 70, size=24, fill='white', bold=True)

    # Form container
    drawRoundedRect(20, 150, app.width - 40, 350, 20, fill='white')

    # Username field
    drawLabel('Username', 50, 180, size=14, fill=app.lightText, align='left')
    fieldBorder = app.primaryColor if app.activeField == 'username' else rgb(200, 200, 200)
    drawRoundedRect(40, 200, app.width - 80, 45, 10, fill='white', border=fieldBorder, borderWidth=2)
    displayText = app.loginUsername if app.loginUsername else 'Enter username'
    textColor = app.textColor if app.loginUsername else app.lightText
    drawLabel(displayText, 55, 222, size=16, fill=textColor, align='left')

    # Password field
    drawLabel('Password', 50, 270, size=14, fill=app.lightText, align='left')
    fieldBorder = app.primaryColor if app.activeField == 'password' else rgb(200, 200, 200)
    drawRoundedRect(40, 290, app.width - 80, 45, 10, fill='white', border=fieldBorder, borderWidth=2)
    displayText = '*' * len(app.loginPassword) if app.loginPassword else 'Enter password'
    textColor = app.textColor if app.loginPassword else app.lightText
    drawLabel(displayText, 55, 312, size=16, fill=textColor, align='left')

    # Error message
    if app.loginError:
        drawLabel(app.loginError, app.width/2, 355, size=14, fill=app.errorColor)

    # Login button
    drawRoundedButton(40, 390, app.width - 80, 50, 'Log In', 'white', app.primaryColor, 25)

    # Sign up link
    drawLabel("Don't have an account?", app.width/2, 470, size=14, fill=app.lightText)
    drawLabel('Sign Up', app.width/2, 495, size=16, fill=app.primaryColor, bold=True)

def drawSignupScreen(app):
    """Draw the signup screen"""
    # Header
    drawRect(0, 0, app.width, 120, fill=app.primaryColor)
    drawLabel('Create Account', app.width/2, 70, size=28, bold=True, fill='white')

    # Back button
    drawLabel('<', 30, 70, size=24, fill='white', bold=True)

    # Form container
    drawRoundedRect(20, 150, app.width - 40, 420, 20, fill='white')

    # Name field
    drawLabel('Full Name', 50, 180, size=14, fill=app.lightText, align='left')
    fieldBorder = app.primaryColor if app.activeField == 'name' else rgb(200, 200, 200)
    drawRoundedRect(40, 200, app.width - 80, 45, 10, fill='white', border=fieldBorder, borderWidth=2)
    displayText = app.signupName if app.signupName else 'Enter your name'
    textColor = app.textColor if app.signupName else app.lightText
    drawLabel(displayText, 55, 222, size=16, fill=textColor, align='left')

    # Username field
    drawLabel('Username', 50, 270, size=14, fill=app.lightText, align='left')
    fieldBorder = app.primaryColor if app.activeField == 'username' else rgb(200, 200, 200)
    drawRoundedRect(40, 290, app.width - 80, 45, 10, fill='white', border=fieldBorder, borderWidth=2)
    displayText = app.signupUsername if app.signupUsername else 'Choose a username'
    textColor = app.textColor if app.signupUsername else app.lightText
    drawLabel(displayText, 55, 312, size=16, fill=textColor, align='left')

    # Password field
    drawLabel('Password', 50, 360, size=14, fill=app.lightText, align='left')
    fieldBorder = app.primaryColor if app.activeField == 'password' else rgb(200, 200, 200)
    drawRoundedRect(40, 380, app.width - 80, 45, 10, fill='white', border=fieldBorder, borderWidth=2)
    displayText = '*' * len(app.signupPassword) if app.signupPassword else 'Create a password'
    textColor = app.textColor if app.signupPassword else app.lightText
    drawLabel(displayText, 55, 402, size=16, fill=textColor, align='left')

    # Error message
    if app.signupError:
        drawLabel(app.signupError, app.width/2, 445, size=14, fill=app.errorColor)

    # Sign up button
    drawRoundedButton(40, 470, app.width - 80, 50, 'Create Account', 'white', app.primaryColor, 25)

    # Login link
    drawLabel('Already have an account?', app.width/2, 550, size=14, fill=app.lightText)
    drawLabel('Log In', app.width/2, 575, size=16, fill=app.primaryColor, bold=True)

def drawPreferencesScreen(app):
    """Draw the preferences/onboarding screen"""
    # Header
    drawRect(0, 0, app.width, 100, fill=app.primaryColor)
    drawLabel('Set Your Preferences', app.width/2, 60, size=22, bold=True, fill='white')

    # Categories section
    drawLabel('What causes interest you?', app.width/2, 130, size=16, fill=app.textColor, bold=True)
    drawLabel('Select all that apply', app.width/2, 150, size=12, fill=app.lightText)

    # Category chips
    chipWidth = 110
    chipHeight = 40
    startX = 35
    startY = 175
    cols = 3

    for i, category in enumerate(app.categories):
        row = i // cols
        col = i % cols
        x = startX + col * (chipWidth + 10)
        y = startY + row * (chipHeight + 12)

        isSelected = category in app.selectedCategories
        bgColor = app.categoryColors[category] if isSelected else rgb(240, 240, 240)
        textColor = 'white' if isSelected else app.textColor

        drawRoundedRect(x, y, chipWidth, chipHeight, 20, fill=bgColor)
        drawLabel(category, x + chipWidth/2, y + chipHeight/2, size=12, fill=textColor, bold=isSelected)

    # Time preference section
    drawLabel('When are you available?', app.width/2, 310, size=16, fill=app.textColor, bold=True)

    timeOptions = [('weekdays', 'Weekdays'), ('weekends', 'Weekends'), ('either', 'Either')]
    optionWidth = 100
    totalWidth = len(timeOptions) * optionWidth + (len(timeOptions) - 1) * 15
    startX = (app.width - totalWidth) / 2

    for i, (value, label) in enumerate(timeOptions):
        x = startX + i * (optionWidth + 15)
        isSelected = app.timePreference == value
        bgColor = app.primaryColor if isSelected else rgb(240, 240, 240)
        textColor = 'white' if isSelected else app.textColor

        drawRoundedRect(x, 340, optionWidth, 45, 22, fill=bgColor)
        drawLabel(label, x + optionWidth/2, 362, size=14, fill=textColor, bold=isSelected)

    # Experience level section
    drawLabel('Your volunteering experience', app.width/2, 420, size=16, fill=app.textColor, bold=True)

    expOptions = [('new', 'New to volunteering'), ('experienced', 'Experienced')]
    optionWidth = 160
    totalWidth = len(expOptions) * optionWidth + 15
    startX = (app.width - totalWidth) / 2

    for i, (value, label) in enumerate(expOptions):
        x = startX + i * (optionWidth + 15)
        isSelected = app.experienceLevel == value
        bgColor = app.secondaryColor if isSelected else rgb(240, 240, 240)
        textColor = 'white' if isSelected else app.textColor

        drawRoundedRect(x, 450, optionWidth, 45, 22, fill=bgColor)
        drawLabel(label, x + optionWidth/2, 472, size=13, fill=textColor, bold=isSelected)

    # Continue button
    canContinue = len(app.selectedCategories) > 0 and app.timePreference is not None
    buttonColor = app.primaryColor if canContinue else rgb(180, 180, 180)
    drawRoundedButton(40, 540, app.width - 80, 50, 'Start Swiping', 'white', buttonColor, 25)

    # Skip link
    drawLabel('Skip for now', app.width/2, 620, size=14, fill=app.lightText)

def drawSwipeScreen(app):
    """Draw the main swipe screen"""
    # Header with profile
    drawRect(0, 0, app.width, 80, fill='white')
    drawLabel('Givr', 30, 45, size=24, bold=True, fill=app.primaryColor, align='left')

    # Profile button
    drawCircle(app.width - 40, 45, 20, fill=rgb(240, 240, 240))
    drawCircle(app.width - 40, 42, 8, fill=app.primaryColor)  # Head
    drawArc(app.width - 40, 60, 24, 16, 0, 180, fill=app.primaryColor)  # Body

    # Check if deck is empty
    remainingEvents = [e for e in app.events if e not in app.savedEvents and e['id'] > app.currentEventIndex]

    if app.currentEventIndex >= len(app.events):
        # Empty deck state
        drawEmptyDeck(app)
    else:
        # Draw current card
        event = app.events[app.currentEventIndex]
        drawSwipeCard(app, event, app.cardOffsetX, app.cardOffsetY)

        # Swipe indicators
        if app.cardOffsetX > 30:
            opacity = min(1, app.cardOffsetX / app.swipeThreshold)
            drawLabel('SAVE', app.width/2, 150, size=32, bold=True,
                     fill=rgb(34, 197, 94), opacity=opacity, rotateAngle=-15)
        elif app.cardOffsetX < -30:
            opacity = min(1, abs(app.cardOffsetX) / app.swipeThreshold)
            drawLabel('SKIP', app.width/2, 150, size=32, bold=True,
                     fill=rgb(239, 68, 68), opacity=opacity, rotateAngle=15)

        # Action buttons
        drawCircle(100, 580, 30, fill='white', border=app.errorColor, borderWidth=3)
        drawLabel('X', 100, 580, size=24, bold=True, fill=app.errorColor)

        drawCircle(app.width - 100, 580, 30, fill='white', border=app.successColor, borderWidth=3)
        drawHeart(app.width - 100, 580, 15, app.successColor)

        # Card counter
        drawLabel(f'{app.currentEventIndex + 1} / {len(app.events)}', app.width/2, 580,
                 size=14, fill=app.lightText)

    # Navigation bar
    drawNavBar(app)

def drawSwipeCard(app, event, offsetX, offsetY):
    """Draw a swipeable event card"""
    cardX = 30 + offsetX
    cardY = 100 + offsetY
    cardWidth = app.width - 60
    cardHeight = 420

    # Card rotation based on drag
    rotation = offsetX * 0.05

    # Card shadow
    drawRoundedRect(cardX + 5, cardY + 5, cardWidth, cardHeight, 20, fill=rgb(220, 220, 220))

    # Main card
    drawRoundedRect(cardX, cardY, cardWidth, cardHeight, 20, fill='white')

    # Category banner
    catColor = app.categoryColors.get(event['category'], app.primaryColor)
    drawRoundedRect(cardX, cardY, cardWidth, 60, 20, fill=catColor)
    drawRect(cardX, cardY + 40, cardWidth, 20, fill=catColor)  # Cover bottom corners

    # Category label
    drawLabel(event['category'].upper(), cardX + 20, cardY + 30, size=12,
             fill='white', align='left', bold=True)

    # Hours badge
    drawRoundedRect(cardX + cardWidth - 70, cardY + 15, 55, 30, 15, fill=rgb(255, 255, 255))
    drawLabel(f"{event['hours']}h", cardX + cardWidth - 42, cardY + 30, size=14, fill='white', bold=True)

    # Event title
    drawLabel(event['title'], cardX + cardWidth/2, cardY + 100, size=22, bold=True, fill=app.textColor)

    # Organization
    drawLabel(event['organization'], cardX + cardWidth/2, cardY + 135, size=14, fill=app.lightText)

    # Divider
    drawLine(cardX + 30, cardY + 165, cardX + cardWidth - 30, cardY + 165, fill=rgb(230, 230, 230))

    # Description
    descLines = wrapText(event['description'], 35)
    for i, line in enumerate(descLines[:3]):
        drawLabel(line, cardX + cardWidth/2, cardY + 195 + i * 22, size=14, fill=app.textColor)

    # Event details
    detailY = cardY + 290

    # Date
    drawCircle(cardX + 40, detailY, 15, fill=rgb(240, 240, 240))
    drawLabel('D', cardX + 40, detailY, size=12, fill=app.primaryColor, bold=True)
    drawLabel(event['date'], cardX + 65, detailY, size=14, fill=app.textColor, align='left')

    # Time
    detailY += 35
    drawCircle(cardX + 40, detailY, 15, fill=rgb(240, 240, 240))
    drawLabel('T', cardX + 40, detailY, size=12, fill=app.primaryColor, bold=True)
    drawLabel(event['timeRange'], cardX + 65, detailY, size=14, fill=app.textColor, align='left')

    # Location
    detailY += 35
    drawCircle(cardX + 40, detailY, 15, fill=rgb(240, 240, 240))
    drawLabel('L', cardX + 40, detailY, size=12, fill=app.primaryColor, bold=True)
    drawLabel(event['location'], cardX + 65, detailY, size=14, fill=app.textColor, align='left')

    # Impact indicator
    drawLabel('Impact:', cardX + 30, cardY + cardHeight - 40, size=12, fill=app.lightText, align='left')
    for i in range(5):
        starColor = rgb(255, 193, 7) if i < event['impactLevel'] else rgb(220, 220, 220)
        drawStar(cardX + 90 + i * 22, cardY + cardHeight - 40, 8, starColor)

def drawEmptyDeck(app):
    """Draw empty deck state"""
    drawCircle(app.width/2, 280, 60, fill=rgb(240, 240, 240))
    drawLabel('!', app.width/2, 280, size=48, fill=app.primaryColor, bold=True)

    drawLabel("You're all caught up!", app.width/2, 370, size=22, bold=True, fill=app.textColor)
    drawLabel('Check back later for more opportunities', app.width/2, 400, size=14, fill=app.lightText)

    # Action buttons
    drawRoundedButton(60, 450, app.width - 120, 45, 'See All Events', 'white', app.primaryColor, 22)
    drawRoundedButton(60, 510, app.width - 120, 45, 'View Saved', app.primaryColor, 'white', 22)

def drawAllEventsScreen(app):
    """Draw all events list screen"""
    # Header
    drawRect(0, 0, app.width, 80, fill='white')
    drawLabel('All Events', app.width/2, 45, size=22, bold=True, fill=app.textColor)

    # Filter chips
    filterY = 100
    filters = ['All'] + app.categories
    chipX = 20
    for filterName in filters:
        chipWidth = len(filterName) * 8 + 20
        isActive = filterName == 'All'  # Default to All
        bgColor = app.primaryColor if isActive else rgb(240, 240, 240)
        textColor = 'white' if isActive else app.textColor

        drawRoundedRect(chipX, filterY, chipWidth, 30, 15, fill=bgColor)
        drawLabel(filterName, chipX + chipWidth/2, filterY + 15, size=11, fill=textColor)
        chipX += chipWidth + 8
        if chipX > app.width - 50:
            break

    # Event list
    listY = 150
    for i, event in enumerate(app.events[:5]):  # Show first 5 for demo
        drawEventListItem(app, event, 20, listY + i * 100, app.width - 40, 90)

    # Navigation bar
    drawNavBar(app)

def drawEventListItem(app, event, x, y, width, height):
    """Draw a compact event list item"""
    # Card background
    drawRoundedRect(x, y, width, height, 15, fill='white')

    # Category indicator
    catColor = app.categoryColors.get(event['category'], app.primaryColor)
    drawRoundedRect(x, y, 8, height, 4, fill=catColor)

    # Title
    drawLabel(event['title'], x + 25, y + 22, size=15, bold=True, fill=app.textColor, align='left')

    # Organization
    drawLabel(event['organization'], x + 25, y + 44, size=12, fill=app.lightText, align='left')

    # Details row
    drawLabel(f"{event['date']}  |  {event['hours']}h  |  {event['location']}",
             x + 25, y + 68, size=11, fill=app.lightText, align='left')

    # Save button
    isSaved = event in app.savedEvents
    btnColor = app.successColor if isSaved else rgb(240, 240, 240)
    iconColor = 'white' if isSaved else app.lightText
    drawCircle(x + width - 35, y + height/2, 20, fill=btnColor)
    drawHeart(x + width - 35, y + height/2, 10, iconColor)

def drawSavedScreen(app):
    """Draw saved events screen"""
    # Header
    drawRect(0, 0, app.width, 80, fill='white')
    drawLabel('Saved Events', app.width/2, 45, size=22, bold=True, fill=app.textColor)

    if len(app.savedEvents) == 0:
        # Empty state
        drawCircle(app.width/2, 280, 50, fill=rgb(240, 240, 240))
        drawHeart(app.width/2, 280, 25, app.lightText)
        drawLabel('No saved events yet', app.width/2, 360, size=18, bold=True, fill=app.textColor)
        drawLabel('Swipe right on events you like!', app.width/2, 390, size=14, fill=app.lightText)
    else:
        # Saved events list
        listY = 100
        for i, event in enumerate(app.savedEvents[:4]):
            drawSavedEventItem(app, event, 20, listY + i * 120, app.width - 40, 110)

    # Navigation bar
    drawNavBar(app)

def drawSavedEventItem(app, event, x, y, width, height):
    """Draw a saved event item with completion status"""
    # Card background
    drawRoundedRect(x, y, width, height, 15, fill='white')

    # Status indicator
    isVerified = event in app.verifiedEvents
    isCompleted = event in app.completedEvents

    if isVerified:
        statusColor = app.successColor
        statusText = 'Verified'
    elif isCompleted:
        statusColor = rgb(255, 193, 7)
        statusText = 'Pending'
    else:
        statusColor = rgb(200, 200, 200)
        statusText = 'Upcoming'

    # Category bar
    catColor = app.categoryColors.get(event['category'], app.primaryColor)
    drawRoundedRect(x, y, 8, height, 4, fill=catColor)

    # Title and org
    drawLabel(event['title'], x + 25, y + 22, size=15, bold=True, fill=app.textColor, align='left')
    drawLabel(event['organization'], x + 25, y + 44, size=12, fill=app.lightText, align='left')

    # Status badge
    badgeWidth = len(statusText) * 7 + 16
    drawRoundedRect(x + width - badgeWidth - 15, y + 15, badgeWidth, 24, 12, fill=statusColor)
    drawLabel(statusText, x + width - badgeWidth/2 - 15, y + 27, size=11, fill='white', bold=True)

    # Details
    drawLabel(f"{event['date']}  |  {event['hours']}h", x + 25, y + 68, size=12, fill=app.lightText, align='left')

    # Action button
    if not isVerified:
        btnText = 'Verify' if isCompleted else 'Mark Done'
        btnColor = app.primaryColor if isCompleted else app.secondaryColor
        drawRoundedRect(x + width - 90, y + height - 35, 75, 28, 14, fill=btnColor)
        drawLabel(btnText, x + width - 52, y + height - 21, size=11, fill='white', bold=True)

def drawMapScreen(app):
    """Draw the map view screen"""
    # Header
    drawRect(0, 0, app.width, 80, fill='white')
    drawLabel('Event Map', app.width/2, 45, size=22, bold=True, fill=app.textColor)

    # Filter toggle
    allActive = app.mapFilter == 'all'
    drawRoundedRect(app.width/2 - 100, 90, 90, 35, 17,
                   fill=app.primaryColor if allActive else rgb(240, 240, 240))
    drawLabel('All Events', app.width/2 - 55, 107, size=12,
             fill='white' if allActive else app.textColor)

    drawRoundedRect(app.width/2 + 10, 90, 90, 35, 17,
                   fill=app.primaryColor if not allActive else rgb(240, 240, 240))
    drawLabel('Saved Only', app.width/2 + 55, 107, size=12,
             fill='white' if not allActive else app.textColor)

    # Map area
    mapY = 140
    mapHeight = 400
    drawRoundedRect(20, mapY, app.width - 40, mapHeight, 15, fill=rgb(230, 235, 240))

    # Draw simplified Pittsburgh neighborhoods
    drawPittsburghMap(app, 20, mapY, app.width - 40, mapHeight)

    # Event pins
    events = app.savedEvents if app.mapFilter == 'saved' else app.events
    for event in events:
        pinX = 20 + (event['mapX'] / 400) * (app.width - 40)
        pinY = mapY + (event['mapY'] / 500) * mapHeight
        catColor = app.categoryColors.get(event['category'], app.primaryColor)

        # Pin shadow
        drawCircle(pinX + 2, pinY + 2, 12, fill=rgb(180, 180, 180))
        # Pin
        drawCircle(pinX, pinY, 12, fill=catColor, border='white', borderWidth=2)

        # Tooltip on hover
        if app.hoveredPin == event['id']:
            drawRoundedRect(pinX - 80, pinY - 60, 160, 50, 10, fill='white')
            drawLabel(event['title'], pinX, pinY - 45, size=11, bold=True, fill=app.textColor)
            drawLabel(f"{event['date']} | {event['hours']}h", pinX, pinY - 25, size=10, fill=app.lightText)

    # Legend
    legendY = mapY + mapHeight + 15
    legendX = 30
    for cat, color in list(app.categoryColors.items())[:3]:
        drawCircle(legendX, legendY, 6, fill=color)
        drawLabel(cat, legendX + 15, legendY, size=10, fill=app.textColor, align='left')
        legendX += 110

    # Navigation bar
    drawNavBar(app)

def drawPittsburghMap(app, x, y, width, height):
    """Draw simplified Pittsburgh neighborhood outlines"""
    # Rivers (simplified)
    drawLine(x, y + height * 0.6, x + width, y + height * 0.4, fill=rgb(100, 149, 237), lineWidth=8)
    drawLine(x + width * 0.3, y + height, x + width * 0.4, y + height * 0.5, fill=rgb(100, 149, 237), lineWidth=6)

    # Neighborhood labels
    neighborhoods = [
        ('Oakland', 0.7, 0.55),
        ('Downtown', 0.35, 0.7),
        ('Shadyside', 0.85, 0.5),
        ('North Shore', 0.3, 0.45),
        ('South Side', 0.4, 0.85)
    ]

    for name, px, py in neighborhoods:
        drawLabel(name, x + width * px, y + height * py, size=10, fill=rgb(100, 100, 100))

def drawRewardsScreen(app):
    """Draw the rewards and progress screen"""
    # Header with gradient
    for i in range(120):
        ratio = i / 120
        r = int(99 + (139 - 99) * ratio)
        g = int(102 + (92 - 102) * ratio)
        b = int(241 + (246 - 241) * ratio)
        drawLine(0, i, app.width, i, fill=rgb(r, g, b))

    drawLabel('Your Impact', app.width/2, 50, size=24, bold=True, fill='white')

    # Stats cards
    drawRoundedRect(20, 90, (app.width - 50) / 2, 80, 15, fill='white')
    drawLabel(str(app.totalHours), 20 + (app.width - 50) / 4, 120, size=28, bold=True, fill=app.primaryColor)
    drawLabel('Verified Hours', 20 + (app.width - 50) / 4, 150, size=12, fill=app.lightText)

    drawRoundedRect(app.width/2 + 5, 90, (app.width - 50) / 2, 80, 15, fill='white')
    drawLabel(str(app.totalPoints), app.width/2 + 5 + (app.width - 50) / 4, 120, size=28, bold=True, fill=app.secondaryColor)
    drawLabel('Impact Points', app.width/2 + 5 + (app.width - 50) / 4, 150, size=12, fill=app.lightText)

    # Tier progress
    tierInfo = app.tiers[app.currentTier]
    nextTier = app.tiers.get(app.currentTier + 1)

    drawRoundedRect(20, 185, app.width - 40, 100, 15, fill='white')
    drawLabel(f"Tier {app.currentTier}: {tierInfo['name']}", app.width/2, 210, size=16, bold=True, fill=app.textColor)

    if nextTier:
        progress = min(1, app.totalPoints / nextTier['minPoints'])
        # Progress bar background
        drawRoundedRect(40, 240, app.width - 80, 16, 8, fill=rgb(230, 230, 230))
        # Progress bar fill
        if progress > 0:
            drawRoundedRect(40, 240, (app.width - 80) * progress, 16, 8, fill=tierInfo['color'])
        drawLabel(f"{nextTier['minPoints'] - app.totalPoints} pts to {nextTier['name']}",
                 app.width/2, 270, size=11, fill=app.lightText)
    else:
        drawLabel('Maximum tier reached!', app.width/2, 250, size=14, fill=app.successColor, bold=True)

    # Streak
    drawRoundedRect(20, 300, app.width - 40, 60, 15, fill='white')
    drawLabel('Weekly Streak', 80, 330, size=14, fill=app.textColor, align='left')
    drawLabel(f'{app.weeklyStreak} weeks', app.width - 80, 330, size=18, bold=True, fill=app.accentColor)

    # Badges section
    drawLabel('Badges', 30, 385, size=16, bold=True, fill=app.textColor, align='left')

    badgeSize = 55
    badgeSpacing = 15
    startX = 30
    startY = 410
    cols = 5

    for i, (badgeId, badge) in enumerate(app.badges.items()):
        row = i // cols
        col = i % cols
        bx = startX + col * (badgeSize + badgeSpacing)
        by = startY + row * (badgeSize + badgeSpacing + 15)

        if badge['unlocked']:
            drawCircle(bx + badgeSize/2, by + badgeSize/2, badgeSize/2, fill=badge['color'])
            drawBadgeIcon(badge['icon'], bx + badgeSize/2, by + badgeSize/2, 15, 'white')
        else:
            drawCircle(bx + badgeSize/2, by + badgeSize/2, badgeSize/2, fill=rgb(220, 220, 220))
            drawLabel('?', bx + badgeSize/2, by + badgeSize/2, size=20, fill='white', bold=True)

        # Badge name (truncated)
        name = badge['name'][:10] + '..' if len(badge['name']) > 10 else badge['name']
        drawLabel(name, bx + badgeSize/2, by + badgeSize + 10, size=8, fill=app.lightText)

    # Navigation bar
    drawNavBar(app)

def drawEventDetailScreen(app):
    """Draw event detail view"""
    if not app.selectedEvent:
        return

    event = app.selectedEvent

    # Header with category color
    catColor = app.categoryColors.get(event['category'], app.primaryColor)
    drawRect(0, 0, app.width, 150, fill=catColor)

    # Back button
    drawCircle(40, 50, 20, fill=rgb(200, 200, 220))
    drawLabel('<', 40, 50, size=20, fill='white', bold=True)

    # Category and hours
    drawLabel(event['category'].upper(), app.width/2, 50, size=12, fill='white', bold=True)
    drawRoundedRect(app.width - 70, 35, 50, 30, 15, fill=rgb(200, 200, 220))
    drawLabel(f"{event['hours']}h", app.width - 45, 50, size=14, fill='white', bold=True)

    # Title
    drawLabel(event['title'], app.width/2, 100, size=22, bold=True, fill='white')
    drawLabel(event['organization'], app.width/2, 130, size=14, fill='white')

    # Content card
    drawRoundedRect(20, 165, app.width - 40, 420, 20, fill='white')

    # Description
    drawLabel('About', 40, 195, size=14, bold=True, fill=app.textColor, align='left')
    descLines = wrapText(event['description'], 40)
    for i, line in enumerate(descLines):
        drawLabel(line, 40, 220 + i * 20, size=13, fill=app.textColor, align='left')

    # Details section
    detailY = 290
    drawLabel('Details', 40, detailY, size=14, bold=True, fill=app.textColor, align='left')

    details = [
        ('Date', event['date']),
        ('Time', event['timeRange']),
        ('Location', event['location']),
        ('Duration', f"{event['hours']} hours"),
        ('Difficulty', 'Easy' if event['difficulty'] == 1 else 'Medium' if event['difficulty'] == 2 else 'Challenging')
    ]

    for i, (label, value) in enumerate(details):
        y = detailY + 30 + i * 35
        drawLabel(label, 40, y, size=12, fill=app.lightText, align='left')
        drawLabel(value, app.width - 60, y, size=13, fill=app.textColor, align='right')
        if i < len(details) - 1:
            drawLine(40, y + 17, app.width - 60, y + 17, fill=rgb(240, 240, 240))

    # Impact rating
    impactY = detailY + 30 + len(details) * 35
    drawLabel('Impact Level', 40, impactY, size=12, fill=app.lightText, align='left')
    for j in range(5):
        starColor = rgb(255, 193, 7) if j < event['impactLevel'] else rgb(220, 220, 220)
        drawStar(app.width - 100 + j * 20, impactY, 8, starColor)

    # Action button
    isSaved = event in app.savedEvents
    btnText = 'Saved!' if isSaved else 'Save Event'
    btnColor = app.successColor if isSaved else app.primaryColor
    drawRoundedButton(40, 600, app.width - 80, 50, btnText, 'white', btnColor, 25)

def drawVerificationScreen(app):
    """Draw verification code entry screen"""
    # Overlay background
    drawRect(0, 0, app.width, app.height, fill=rgb(50, 50, 50))

    # Modal
    modalY = 200
    modalHeight = 300
    drawRoundedRect(30, modalY, app.width - 60, modalHeight, 20, fill='white')

    # Close button
    drawCircle(app.width - 50, modalY + 20, 15, fill=rgb(240, 240, 240))
    drawLabel('X', app.width - 50, modalY + 20, size=14, fill=app.textColor, bold=True)

    # Title
    drawLabel('Verify Attendance', app.width/2, modalY + 50, size=20, bold=True, fill=app.textColor)

    if app.verificationEvent:
        drawLabel(app.verificationEvent['title'], app.width/2, modalY + 80, size=14, fill=app.lightText)

    # Instructions
    drawLabel('Enter the 4-character code', app.width/2, modalY + 115, size=13, fill=app.textColor)
    drawLabel('provided by the organizer:', app.width/2, modalY + 135, size=13, fill=app.textColor)

    # Code input boxes
    boxSize = 50
    boxSpacing = 15
    totalWidth = 4 * boxSize + 3 * boxSpacing
    startX = (app.width - totalWidth) / 2

    for i in range(4):
        x = startX + i * (boxSize + boxSpacing)
        drawRoundedRect(x, modalY + 160, boxSize, boxSize, 10, fill=rgb(245, 245, 250),
                       border=app.primaryColor, borderWidth=2)
        if i < len(app.verificationCode):
            drawLabel(app.verificationCode[i].upper(), x + boxSize/2, modalY + 185,
                     size=24, bold=True, fill=app.textColor)

    # Error message
    if app.verificationError:
        drawLabel(app.verificationError, app.width/2, modalY + 230, size=13, fill=app.errorColor)

    # Verify button
    canVerify = len(app.verificationCode) == 4
    btnColor = app.primaryColor if canVerify else rgb(180, 180, 180)
    drawRoundedButton(60, modalY + 250, app.width - 120, 40, 'Verify', 'white', btnColor, 20)

def drawProfileScreen(app):
    """Draw user profile screen"""
    # Header
    drawRect(0, 0, app.width, 180, fill=app.primaryColor)

    # Back button
    drawLabel('<', 30, 50, size=24, fill='white', bold=True)
    drawLabel('Profile', app.width/2, 50, size=20, bold=True, fill='white')

    # Profile avatar
    drawCircle(app.width/2, 130, 50, fill='white')
    drawCircle(app.width/2, 120, 20, fill=app.primaryColor)
    drawArc(app.width/2, 155, 50, 30, 0, 180, fill=app.primaryColor)

    # User info card
    drawRoundedRect(20, 200, app.width - 40, 120, 15, fill='white')

    if app.currentUser:
        userName = app.users[app.currentUser].get('name', app.currentUser)
        drawLabel(userName, app.width/2, 235, size=20, bold=True, fill=app.textColor)
        drawLabel(f'@{app.currentUser}', app.width/2, 260, size=14, fill=app.lightText)

        # Member since
        drawLabel('Member since Nov 2024', app.width/2, 295, size=12, fill=app.lightText)

    # Stats summary
    drawRoundedRect(20, 340, app.width - 40, 100, 15, fill='white')

    stats = [
        (str(len(app.verifiedEvents)), 'Events'),
        (str(app.totalHours), 'Hours'),
        (str(app.totalPoints), 'Points')
    ]

    statWidth = (app.width - 40) / 3
    for i, (value, label) in enumerate(stats):
        x = 20 + statWidth * i + statWidth / 2
        drawLabel(value, x, 375, size=24, bold=True, fill=app.primaryColor)
        drawLabel(label, x, 405, size=12, fill=app.lightText)

    # Settings options
    options = ['Edit Preferences', 'Notification Settings', 'Help & Support', 'Log Out']
    optionY = 470

    for option in options:
        drawRoundedRect(20, optionY, app.width - 40, 50, 10, fill='white')
        drawLabel(option, 40, optionY + 25, size=14, fill=app.textColor if option != 'Log Out' else app.errorColor, align='left')
        drawLabel('>', app.width - 50, optionY + 25, size=16, fill=app.lightText)
        optionY += 60

def drawNavBar(app):
    """Draw bottom navigation bar"""
    navY = app.height - 70
    drawRect(0, navY, app.width, 70, fill='white')
    drawLine(0, navY, app.width, navY, fill=rgb(230, 230, 230))

    itemWidth = app.width / 5

    # Determine active tab
    modeToTab = {
        'swipe': 0,
        'allEvents': 1,
        'saved': 2,
        'map': 3,
        'rewards': 4
    }
    activeTab = modeToTab.get(app.mode, 0)

    for i, (name, icon) in enumerate(zip(app.navItems, app.navIcons)):
        x = itemWidth * i + itemWidth / 2
        y = navY + 35

        isActive = i == activeTab
        color = app.primaryColor if isActive else app.lightText

        # Icon
        drawNavIcon(icon, x, y - 10, isActive, color)

        # Label
        drawLabel(name, x, y + 18, size=10, fill=color, bold=isActive)

def drawNavIcon(icon, x, y, isActive, color):
    """Draw navigation icons"""
    if icon == 'swipe':
        # Cards icon
        drawRoundedRect(x - 10, y - 8, 14, 18, 3, fill=None, border=color, borderWidth=2)
        drawRoundedRect(x - 4, y - 10, 14, 18, 3, fill=color if isActive else None, border=color, borderWidth=2)
    elif icon == 'list':
        # List icon
        for i in range(3):
            drawLine(x - 10, y - 8 + i * 8, x + 10, y - 8 + i * 8, fill=color, lineWidth=2)
    elif icon == 'heart':
        drawHeart(x, y, 12, color)
    elif icon == 'map':
        # Map pin icon
        drawCircle(x, y - 5, 8, fill=None, border=color, borderWidth=2)
        drawCircle(x, y - 5, 3, fill=color)
        drawPolygon(x - 4, y, x + 4, y, x, y + 10, fill=color)
    elif icon == 'star':
        drawStar(x, y, 12, color)

# ============================================================================
# HELPER DRAWING FUNCTIONS
# ============================================================================

def drawRoundedRect(x, y, width, height, radius, fill='white', border=None, borderWidth=1):
    """Draw a rounded rectangle"""
    # Clamp radius to avoid negative dimensions
    radius = min(radius, width / 2, height / 2)

    # Draw the main body
    innerWidth = width - 2 * radius
    innerHeight = height - 2 * radius

    if innerWidth > 0:
        drawRect(x + radius, y, innerWidth, height, fill=fill)
    if innerHeight > 0:
        drawRect(x, y + radius, width, innerHeight, fill=fill)

    # Draw corner circles
    drawCircle(x + radius, y + radius, radius, fill=fill)
    drawCircle(x + width - radius, y + radius, radius, fill=fill)
    drawCircle(x + radius, y + height - radius, radius, fill=fill)
    drawCircle(x + width - radius, y + height - radius, radius, fill=fill)

    if border:
        # Draw border using lines and arcs
        drawArc(x + radius, y + radius, radius*2, radius*2, 90, 90, fill=None, border=border, borderWidth=borderWidth)
        drawArc(x + width - radius, y + radius, radius*2, radius*2, 0, 90, fill=None, border=border, borderWidth=borderWidth)
        drawArc(x + radius, y + height - radius, radius*2, radius*2, 180, 90, fill=None, border=border, borderWidth=borderWidth)
        drawArc(x + width - radius, y + height - radius, radius*2, radius*2, 270, 90, fill=None, border=border, borderWidth=borderWidth)
        if innerWidth > 0:
            drawLine(x + radius, y, x + width - radius, y, fill=border, lineWidth=borderWidth)
            drawLine(x + radius, y + height, x + width - radius, y + height, fill=border, lineWidth=borderWidth)
        if innerHeight > 0:
            drawLine(x, y + radius, x, y + height - radius, fill=border, lineWidth=borderWidth)
            drawLine(x + width, y + radius, x + width, y + height - radius, fill=border, lineWidth=borderWidth)

def drawRoundedButton(x, y, width, height, text, textColor, bgColor, radius):
    """Draw a rounded button with text"""
    drawRoundedRect(x, y, width, height, radius, fill=bgColor)
    drawLabel(text, x + width/2, y + height/2, size=16, bold=True, fill=textColor)

def drawHeart(x, y, size, color):
    """Draw a heart shape"""
    s = size / 10
    # Left curve
    drawCircle(x - s*3, y - s*2, s*4, fill=color)
    # Right curve
    drawCircle(x + s*3, y - s*2, s*4, fill=color)
    # Bottom triangle
    drawPolygon(x - s*6.5, y, x + s*6.5, y, x, y + s*8, fill=color)

def drawStar(x, y, size, color):
    """Draw a 5-pointed star"""
    points = []
    for i in range(10):
        angle = i * 36 - 90
        r = size if i % 2 == 0 else size * 0.4
        px = x + r * math.cos(math.radians(angle))
        py = y + r * math.sin(math.radians(angle))
        points.extend([px, py])
    drawPolygon(*points, fill=color)

def drawBadgeIcon(icon, x, y, size, color):
    """Draw badge icons"""
    if icon == 'star':
        drawStar(x, y, size, color)
    elif icon == 'sun':
        drawCircle(x, y, size * 0.6, fill=color)
        for i in range(8):
            angle = i * 45
            x1 = x + size * 0.7 * math.cos(math.radians(angle))
            y1 = y + size * 0.7 * math.sin(math.radians(angle))
            x2 = x + size * math.cos(math.radians(angle))
            y2 = y + size * math.sin(math.radians(angle))
            drawLine(x1, y1, x2, y2, fill=color, lineWidth=2)
    elif icon == 'leaf':
        drawOval(x, y, size * 1.2, size * 2, fill=color, rotateAngle=30)
    elif icon == 'book':
        drawRect(x - size * 0.6, y - size * 0.5, size * 1.2, size, fill=color)
        drawLine(x, y - size * 0.5, x, y + size * 0.5, fill='white', lineWidth=2)
    elif icon == 'clock':
        drawCircle(x, y, size, fill=None, border=color, borderWidth=2)
        drawLine(x, y, x, y - size * 0.5, fill=color, lineWidth=2)
        drawLine(x, y, x + size * 0.4, y, fill=color, lineWidth=2)
    elif icon == 'map':
        drawCircle(x, y - size * 0.3, size * 0.6, fill=color)
        drawPolygon(x - size * 0.4, y, x + size * 0.4, y, x, y + size * 0.7, fill=color)

def wrapText(text, maxChars):
    """Wrap text to fit within maxChars per line"""
    words = text.split()
    lines = []
    currentLine = ''

    for word in words:
        if len(currentLine) + len(word) + 1 <= maxChars:
            currentLine += (' ' if currentLine else '') + word
        else:
            if currentLine:
                lines.append(currentLine)
            currentLine = word

    if currentLine:
        lines.append(currentLine)

    return lines

# ============================================================================
# EVENT HANDLERS
# ============================================================================

def onMousePress(app, mouseX, mouseY):
    if app.mode == 'intro':
        handleIntroClick(app, mouseX, mouseY)
    elif app.mode == 'login':
        handleLoginClick(app, mouseX, mouseY)
    elif app.mode == 'signup':
        handleSignupClick(app, mouseX, mouseY)
    elif app.mode == 'preferences':
        handlePreferencesClick(app, mouseX, mouseY)
    elif app.mode == 'swipe':
        handleSwipePress(app, mouseX, mouseY)
    elif app.mode == 'allEvents':
        handleAllEventsClick(app, mouseX, mouseY)
    elif app.mode == 'saved':
        handleSavedClick(app, mouseX, mouseY)
    elif app.mode == 'map':
        handleMapClick(app, mouseX, mouseY)
    elif app.mode == 'rewards':
        handleRewardsClick(app, mouseX, mouseY)
    elif app.mode == 'eventDetail':
        handleEventDetailClick(app, mouseX, mouseY)
    elif app.mode == 'verification':
        handleVerificationClick(app, mouseX, mouseY)
    elif app.mode == 'profile':
        handleProfileClick(app, mouseX, mouseY)

    # Check nav bar clicks (except on certain screens)
    if app.mode in ['swipe', 'allEvents', 'saved', 'map', 'rewards']:
        handleNavClick(app, mouseX, mouseY)

def onMouseDrag(app, mouseX, mouseY):
    if app.mode == 'swipe' and app.isDragging:
        app.cardOffsetX = mouseX - app.dragStartX
        app.cardOffsetY = (mouseY - app.dragStartY) * 0.3  # Reduced vertical movement

def onMouseRelease(app, mouseX, mouseY):
    if app.mode == 'swipe' and app.isDragging:
        app.isDragging = False

        if app.cardOffsetX > app.swipeThreshold:
            # Swipe right - save event
            if app.currentEventIndex < len(app.events):
                event = app.events[app.currentEventIndex]
                if event not in app.savedEvents:
                    app.savedEvents.append(event)
                app.currentEventIndex += 1
        elif app.cardOffsetX < -app.swipeThreshold:
            # Swipe left - skip event
            app.currentEventIndex += 1

        # Reset card position
        app.cardOffsetX = 0
        app.cardOffsetY = 0

def onKeyPress(app, key):
    if app.mode == 'login':
        handleLoginKeyPress(app, key)
    elif app.mode == 'signup':
        handleSignupKeyPress(app, key)
    elif app.mode == 'verification':
        handleVerificationKeyPress(app, key)
    elif app.mode == 'swipe':
        # Keyboard shortcuts for swiping
        if key == 'left' and app.currentEventIndex < len(app.events):
            app.currentEventIndex += 1
        elif key == 'right' and app.currentEventIndex < len(app.events):
            event = app.events[app.currentEventIndex]
            if event not in app.savedEvents:
                app.savedEvents.append(event)
            app.currentEventIndex += 1

# ============================================================================
# CLICK HANDLERS
# ============================================================================

def handleIntroClick(app, mouseX, mouseY):
    # Get Started button
    if 530 <= mouseY <= 580 and app.width/2 - 120 <= mouseX <= app.width/2 + 120:
        app.mode = 'signup'
    # Login link
    elif 595 <= mouseY <= 625:
        app.mode = 'login'

def handleLoginClick(app, mouseX, mouseY):
    # Back button
    if mouseY <= 100 and mouseX <= 60:
        app.mode = 'intro'
        return

    # Username field
    if 200 <= mouseY <= 245:
        app.activeField = 'username'
    # Password field
    elif 290 <= mouseY <= 335:
        app.activeField = 'password'
    # Login button
    elif 390 <= mouseY <= 440:
        attemptLogin(app)
    # Sign up link
    elif 480 <= mouseY <= 510:
        app.mode = 'signup'
        app.activeField = None
    else:
        app.activeField = None

def handleSignupClick(app, mouseX, mouseY):
    # Back button
    if mouseY <= 100 and mouseX <= 60:
        app.mode = 'intro'
        return

    # Name field
    if 200 <= mouseY <= 245:
        app.activeField = 'name'
    # Username field
    elif 290 <= mouseY <= 335:
        app.activeField = 'username'
    # Password field
    elif 380 <= mouseY <= 425:
        app.activeField = 'password'
    # Sign up button
    elif 470 <= mouseY <= 520:
        attemptSignup(app)
    # Login link
    elif 560 <= mouseY <= 590:
        app.mode = 'login'
        app.activeField = None
    else:
        app.activeField = None

def handlePreferencesClick(app, mouseX, mouseY):
    # Category chips
    chipWidth = 110
    chipHeight = 40
    startX = 35
    startY = 175
    cols = 3

    for i, category in enumerate(app.categories):
        row = i // cols
        col = i % cols
        x = startX + col * (chipWidth + 10)
        y = startY + row * (chipHeight + 12)

        if x <= mouseX <= x + chipWidth and y <= mouseY <= y + chipHeight:
            if category in app.selectedCategories:
                app.selectedCategories.remove(category)
            else:
                app.selectedCategories.add(category)
            return

    # Time preference buttons
    timeOptions = ['weekdays', 'weekends', 'either']
    optionWidth = 100
    totalWidth = len(timeOptions) * optionWidth + (len(timeOptions) - 1) * 15
    startX = (app.width - totalWidth) / 2

    for i, value in enumerate(timeOptions):
        x = startX + i * (optionWidth + 15)
        if x <= mouseX <= x + optionWidth and 340 <= mouseY <= 385:
            app.timePreference = value
            return

    # Experience level buttons
    expOptions = ['new', 'experienced']
    optionWidth = 160
    totalWidth = len(expOptions) * optionWidth + 15
    startX = (app.width - totalWidth) / 2

    for i, value in enumerate(expOptions):
        x = startX + i * (optionWidth + 15)
        if x <= mouseX <= x + optionWidth and 450 <= mouseY <= 495:
            app.experienceLevel = value
            return

    # Continue button
    if 540 <= mouseY <= 590 and 40 <= mouseX <= app.width - 40:
        if len(app.selectedCategories) > 0 and app.timePreference is not None:
            app.mode = 'swipe'

    # Skip link
    if 605 <= mouseY <= 635:
        app.mode = 'swipe'

def handleSwipePress(app, mouseX, mouseY):
    # Profile button
    if 25 <= mouseY <= 65 and app.width - 60 <= mouseX <= app.width - 20:
        app.mode = 'profile'
        return

    # Check if deck is empty
    if app.currentEventIndex >= len(app.events):
        # See All Events button
        if 450 <= mouseY <= 495:
            app.mode = 'allEvents'
        # View Saved button
        elif 510 <= mouseY <= 555:
            app.mode = 'saved'
        return

    # Skip button (X)
    if 550 <= mouseY <= 610 and 70 <= mouseX <= 130:
        app.currentEventIndex += 1
        return

    # Save button (heart)
    if 550 <= mouseY <= 610 and app.width - 130 <= mouseX <= app.width - 70:
        event = app.events[app.currentEventIndex]
        if event not in app.savedEvents:
            app.savedEvents.append(event)
        app.currentEventIndex += 1
        return

    # Start dragging card
    if 100 <= mouseY <= 520 and 30 <= mouseX <= app.width - 30:
        app.isDragging = True
        app.dragStartX = mouseX
        app.dragStartY = mouseY

def handleAllEventsClick(app, mouseX, mouseY):
    # Event list items
    listY = 150
    for i, event in enumerate(app.events[:5]):
        itemY = listY + i * 100
        if itemY <= mouseY <= itemY + 90:
            # Save button
            if app.width - 55 <= mouseX <= app.width - 15:
                if event in app.savedEvents:
                    app.savedEvents.remove(event)
                else:
                    app.savedEvents.append(event)
            else:
                # Open event detail
                app.selectedEvent = event
                app.detailSource = 'allEvents'
                app.mode = 'eventDetail'
            return

def handleSavedClick(app, mouseX, mouseY):
    # Saved event items
    listY = 100
    for i, event in enumerate(app.savedEvents[:4]):
        itemY = listY + i * 120
        if itemY <= mouseY <= itemY + 110:
            # Verify/Mark Done button
            if app.width - 110 <= mouseX <= app.width - 35 and itemY + 75 <= mouseY <= itemY + 103:
                if event in app.completedEvents and event not in app.verifiedEvents:
                    # Open verification
                    app.verificationEvent = event
                    app.verificationCode = ''
                    app.verificationError = ''
                    app.mode = 'verification'
                elif event not in app.completedEvents:
                    # Mark as completed
                    app.completedEvents.append(event)
            else:
                # Open event detail
                app.selectedEvent = event
                app.detailSource = 'saved'
                app.mode = 'eventDetail'
            return

def handleMapClick(app, mouseX, mouseY):
    # Filter toggle
    if 90 <= mouseY <= 125:
        if app.width/2 - 100 <= mouseX <= app.width/2 - 10:
            app.mapFilter = 'all'
        elif app.width/2 + 10 <= mouseX <= app.width/2 + 100:
            app.mapFilter = 'saved'
        return

    # Event pins
    mapY = 140
    mapHeight = 400
    events = app.savedEvents if app.mapFilter == 'saved' else app.events

    for event in events:
        pinX = 20 + (event['mapX'] / 400) * (app.width - 40)
        pinY = mapY + (event['mapY'] / 500) * mapHeight

        if abs(mouseX - pinX) <= 15 and abs(mouseY - pinY) <= 15:
            if app.hoveredPin == event['id']:
                # Open detail
                app.selectedEvent = event
                app.detailSource = 'map'
                app.mode = 'eventDetail'
            else:
                app.hoveredPin = event['id']
            return

    app.hoveredPin = None

def handleRewardsClick(app, mouseX, mouseY):
    pass  # Rewards screen is mostly display-only

def handleEventDetailClick(app, mouseX, mouseY):
    event = app.selectedEvent

    # Back button
    if mouseY <= 80 and mouseX <= 60:
        app.mode = app.detailSource or 'swipe'
        app.selectedEvent = None
        return

    # Save button
    if 600 <= mouseY <= 650:
        if event not in app.savedEvents:
            app.savedEvents.append(event)

def handleVerificationClick(app, mouseX, mouseY):
    modalY = 200

    # Close button
    if abs(mouseX - (app.width - 50)) <= 15 and abs(mouseY - (modalY + 20)) <= 15:
        app.mode = 'saved'
        app.verificationEvent = None
        return

    # Verify button
    if modalY + 250 <= mouseY <= modalY + 290 and len(app.verificationCode) == 4:
        attemptVerification(app)

def handleProfileClick(app, mouseX, mouseY):
    # Back button
    if mouseY <= 80 and mouseX <= 60:
        app.mode = 'swipe'
        return

    # Log out option
    if 650 <= mouseY <= 700:
        logout(app)

def handleNavClick(app, mouseX, mouseY):
    navY = app.height - 70

    if mouseY >= navY:
        itemWidth = app.width / 5
        tabIndex = int(mouseX // itemWidth)

        modes = ['swipe', 'allEvents', 'saved', 'map', 'rewards']
        if 0 <= tabIndex < len(modes):
            app.mode = modes[tabIndex]

# ============================================================================
# KEY HANDLERS
# ============================================================================

def handleLoginKeyPress(app, key):
    if app.activeField == 'username':
        if key == 'backspace':
            app.loginUsername = app.loginUsername[:-1]
        elif key == 'tab':
            app.activeField = 'password'
        elif key == 'enter':
            attemptLogin(app)
        elif len(key) == 1 and key.isalnum():
            app.loginUsername += key
    elif app.activeField == 'password':
        if key == 'backspace':
            app.loginPassword = app.loginPassword[:-1]
        elif key == 'tab':
            app.activeField = 'username'
        elif key == 'enter':
            attemptLogin(app)
        elif len(key) == 1:
            app.loginPassword += key

def handleSignupKeyPress(app, key):
    if app.activeField == 'name':
        if key == 'backspace':
            app.signupName = app.signupName[:-1]
        elif key == 'tab':
            app.activeField = 'username'
        elif key == 'space':
            app.signupName += ' '
        elif len(key) == 1 and (key.isalpha() or key == ' '):
            app.signupName += key
    elif app.activeField == 'username':
        if key == 'backspace':
            app.signupUsername = app.signupUsername[:-1]
        elif key == 'tab':
            app.activeField = 'password'
        elif len(key) == 1 and key.isalnum():
            app.signupUsername += key
    elif app.activeField == 'password':
        if key == 'backspace':
            app.signupPassword = app.signupPassword[:-1]
        elif key == 'tab':
            app.activeField = 'name'
        elif key == 'enter':
            attemptSignup(app)
        elif len(key) == 1:
            app.signupPassword += key

def handleVerificationKeyPress(app, key):
    if key == 'backspace':
        app.verificationCode = app.verificationCode[:-1]
        app.verificationError = ''
    elif key == 'enter' and len(app.verificationCode) == 4:
        attemptVerification(app)
    elif key == 'escape':
        app.mode = 'saved'
        app.verificationEvent = None
    elif len(key) == 1 and key.isalnum() and len(app.verificationCode) < 4:
        app.verificationCode += key.upper()
        app.verificationError = ''

# ============================================================================
# AUTH & VERIFICATION FUNCTIONS
# ============================================================================

def attemptLogin(app):
    if not app.loginUsername or not app.loginPassword:
        app.loginError = 'Please fill in all fields'
        return

    if app.loginUsername in app.users:
        if app.users[app.loginUsername]['password'] == app.loginPassword:
            app.isLoggedIn = True
            app.currentUser = app.loginUsername
            app.loginError = ''
            app.loginUsername = ''
            app.loginPassword = ''
            app.mode = 'preferences'
            return

    app.loginError = 'Invalid username or password'

def attemptSignup(app):
    if not app.signupName or not app.signupUsername or not app.signupPassword:
        app.signupError = 'Please fill in all fields'
        return

    if app.signupUsername in app.users:
        app.signupError = 'Username already taken'
        return

    if len(app.signupPassword) < 4:
        app.signupError = 'Password must be at least 4 characters'
        return

    # Create new user
    app.users[app.signupUsername] = {
        'password': app.signupPassword,
        'name': app.signupName,
        'preferences': {},
        'stats': {'points': 0, 'hours': 0}
    }

    app.isLoggedIn = True
    app.currentUser = app.signupUsername
    app.signupError = ''
    app.signupName = ''
    app.signupUsername = ''
    app.signupPassword = ''
    app.mode = 'preferences'

def attemptVerification(app):
    if not app.verificationEvent:
        return

    correctCode = app.verificationEvent['verificationCode']

    if app.verificationCode.upper() == correctCode.upper():
        # Success!
        event = app.verificationEvent
        app.verifiedEvents.append(event)

        # Update rewards
        points = calculatePoints(event)
        app.totalPoints += points
        app.totalHours += event['hours']

        # Update tier
        updateTier(app)

        # Update badges
        updateBadges(app, event)

        # Update streak
        app.weeklyStreak += 1

        # Return to saved screen
        app.mode = 'saved'
        app.verificationEvent = None
        app.verificationCode = ''
    else:
        app.verificationError = 'Incorrect code. Try again.'

def logout(app):
    app.isLoggedIn = False
    app.currentUser = None
    app.loginUsername = ''
    app.loginPassword = ''
    app.mode = 'intro'

def calculatePoints(event):
    """Calculate impact points for an event"""
    basePoints = event['hours'] * 10
    difficultyMultiplier = 1 + (event['difficulty'] - 1) * 0.25
    impactMultiplier = 1 + (event['impactLevel'] - 1) * 0.2
    return int(basePoints * difficultyMultiplier * impactMultiplier)

def updateTier(app):
    """Update user tier based on points"""
    for tier in range(4, 0, -1):
        if app.totalPoints >= app.tiers[tier]['minPoints']:
            app.currentTier = tier
            break

def updateBadges(app, event):
    """Update badge progress and unlocks"""
    # Getting Started badge
    if len(app.verifiedEvents) == 1:
        app.badges['getting_started']['unlocked'] = True

    # Weekend Warrior (check if weekend event)
    if 'Sat' in event['date'] or 'Sun' in event['date']:
        app.badges['weekend_warrior']['progress'] = app.badges['weekend_warrior'].get('progress', 0) + 1
        if app.badges['weekend_warrior']['progress'] >= 3:
            app.badges['weekend_warrior']['unlocked'] = True

    # Category-specific badges
    if event['category'] == 'Environment':
        app.badges['green_guardian']['progress'] = app.badges['green_guardian'].get('progress', 0) + 1
        if app.badges['green_guardian']['progress'] >= 5:
            app.badges['green_guardian']['unlocked'] = True

    if event['category'] == 'Education':
        app.badges['kids_champion']['progress'] = app.badges['kids_champion'].get('progress', 0) + 1
        if app.badges['kids_champion']['progress'] >= 5:
            app.badges['kids_champion']['unlocked'] = True

    # Marathon Volunteer
    app.badges['marathon_volunteer']['progress'] = app.totalHours
    if app.totalHours >= 20:
        app.badges['marathon_volunteer']['unlocked'] = True

    # Neighborhood Navigator
    locations = set(e['location'] for e in app.verifiedEvents)
    app.badges['neighborhood_navigator']['progress'] = len(locations)
    if len(locations) >= 3:
        app.badges['neighborhood_navigator']['unlocked'] = True

# ============================================================================
# RUN THE APP
# ============================================================================

def main():
    runApp(width=400, height=700)

main()
