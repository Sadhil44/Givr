from cmu_graphics import *
import math
import os
import json
import AI_givr


def onAppStart(app):
    app.width = 400  # Change the viewer to be like a cell phone
    app.height = 700

    # Navigation state
    app.mode = 'intro'   # app starts at intro

    # User state
    app.isLoggedIn = False
    app.currentUser = None   # current user
    app.userType = None  # 'volunteer' or 'organizer'
    app.users = {}  #set of all users

    # Organizer accounts (pre-populated)
    app.organizers = {
        'pghparks': {'password': 'parks123', 'name': 'Pittsburgh Parks', 'org': 'Pittsburgh Parks'},
        'cmututor': {'password': 'tutor123', 'name': 'CMU Tutoring', 'org': 'CMU Tutoring'},
        'foodbank': {'password': 'food123', 'name': 'PGH Food Bank', 'org': 'PGH Food Bank'},
        'senior': {'password': 'senior123', 'name': 'Senior Center', 'org': 'Senior Center'},
        'arts': {'password': 'arts123', 'name': 'Arts Council', 'org': 'Arts Council'},
    }

    # Form state
    app.loginUsername = ''
    app.loginPassword = ''
    app.signupUsername = ''
    app.signupPassword = ''
    app.signupName = ''
    app.signupOrgName = ''  # For organizer signup
    app.activeField = None
    app.loginError = ''
    app.signupError = ''
    app.loginType = 'volunteer'  # 'volunteer' or 'organizer'
    app.signupType = 'volunteer'  # 'volunteer' or 'organizer'

    # Organizer state
    app.selectedOrgEvent = None

    # Event creation state
    app.newEventTitle = ''
    app.newEventDesc = ''
    app.newEventDate = ''
    app.newEventTime = ''
    app.newEventLocation = ''
    app.newEventHours = ''
    app.newEventCategory = None
    app.newEventImpact = 3
    app.createEventField = None
    app.createEventError = ''

    # Preferences
    app.categories = ['Environment', 'Education', 'Community', 'Health', 'Arts']
    app.categoryColors = {
        'Environment': 'green',
        'Education': 'dodgerBlue',
        'Community': 'orange',
        'Health': 'crimson',
        'Arts': 'purple'
    }
    app.selectedCategories = set()
    app.timePreference = None
    app.experienceLevel = None

    # Events data
    app.events = createEvents()
    app.currentEventIndex = 0
    app.savedEvents = []
    app.completedEvents = []
    app.verifiedEvents = []

    # Swipe state
    app.isDragging = False
    app.dragStartX = 0
    app.cardOffsetX = 0
    app.swipeThreshold = 80

    #AI Event Generation
    app.aiEnabled = True
    app.minEventsBeforeGenerate = 2  # Generate more when this many events left

    # Detail view
    app.selectedEvent = None
    app.detailSource = None

    # Verification
    app.verificationEvent = None
    app.verificationCode = ''
    app.verificationError = ''

    # Rewards
    app.totalPoints = 0
    app.totalHours = 0
    app.currentTier = 1
    app.tierNames = ['New Giver', 'Community Builder', 'Impact Leader', 'Civic Champion']
    app.tierThresholds = [0, 100, 300, 600]
    app.weeklyStreak = 0

    # Badges
    app.badges = {
        'first_event': {'name': 'First Event', 'unlocked': False},
        'weekend_warrior': {'name': 'Weekend Warrior', 'unlocked': False, 'progress': 0},
        'five_hours': {'name': '5 Hours', 'unlocked': False},
        'three_locations': {'name': 'Explorer', 'unlocked': False}
    }

def createEvents():
    if os.path.exists('events.json'):
        f = open('events.json', 'r')
        events = json.load(f)
        f.close()
        return events
    else:
        return createSampleEvents()

def createSampleEvents():
    # Each event has an 'icon' that represents the event visually
    # Icons are drawn using shapes (trees, books, hearts, etc.)
    return [
        {
            'id': 1, 'title': 'Park Cleanup',
            'org': 'Pittsburgh Parks', 'category': 'Environment',
            'desc': 'Help clean up Schenley Park and make it beautiful for everyone',
            'hours': 3, 'date': 'Sat, Nov 25', 'time': '10AM-1PM',
            'location': 'Oakland', 'mapX': 280, 'mapY': 320,
            'impact': 3, 'code': 'PARK', 'icon': 'tree'
        },
        {
            'id': 2, 'title': 'Youth Tutoring',
            'org': 'CMU Tutoring', 'category': 'Education',
            'desc': 'Help middle school students succeed in math and reading',
            'hours': 2, 'date': 'Mon, Nov 27', 'time': '4PM-6PM',
            'location': 'East Liberty', 'mapX': 320, 'mapY': 250,
            'impact': 4, 'code': 'TUTR', 'icon': 'book'
        },
        {
            'id': 3, 'title': 'Food Bank',
            'org': 'PGH Food Bank', 'category': 'Community',
            'desc': 'Sort and pack food donations to help families in need',
            'hours': 4, 'date': 'Sun, Nov 26', 'time': '9AM-1PM',
            'location': 'Downtown', 'mapX': 150, 'mapY': 400,
            'impact': 5, 'code': 'FOOD', 'icon': 'box'
        },
        {
            'id': 4, 'title': 'Senior Visit',
            'org': 'Senior Center', 'category': 'Health',
            'desc': 'Bring joy to seniors through conversation and games',
            'hours': 2, 'date': 'Wed, Nov 29', 'time': '2PM-4PM',
            'location': 'Friendship', 'mapX': 300, 'mapY': 280,
            'impact': 4, 'code': 'SNRS', 'icon': 'heart'
        },
        {
            'id': 5, 'title': 'Art Workshop',
            'org': 'Arts Council', 'category': 'Arts',
            'desc': 'Help kids discover their creativity through painting',
            'hours': 3, 'date': 'Sat, Dec 2', 'time': '1PM-4PM',
            'location': 'Shadyside', 'mapX': 340, 'mapY': 300,
            'impact': 3, 'code': 'ARTS', 'icon': 'palette'
        },
        {
            'id': 6, 'title': 'Trail Cleanup',
            'org': 'Heritage Trail', 'category': 'Environment',
            'desc': 'Keep our riverfront trails clean and accessible',
            'hours': 4, 'date': 'Sat, Dec 9', 'time': '8AM-12PM',
            'location': 'North Shore', 'mapX': 120, 'mapY': 280,
            'impact': 4, 'code': 'RIVR', 'icon': 'tree'
        },
        {
            'id': 7, 'title': 'Homework Help',
            'org': 'Boys & Girls Club', 'category': 'Education',
            'desc': 'Support young students with their after-school homework',
            'hours': 2, 'date': 'Tue, Nov 28', 'time': '3:30PM-5:30PM',
            'location': 'Hill District', 'mapX': 180, 'mapY': 350,
            'impact': 4, 'code': 'HMWK', 'icon': 'book'
        },
        {
            'id': 8, 'title': 'Mural Project',
            'org': 'Sprout Fund', 'category': 'Arts',
            'desc': 'Create a beautiful mural to brighten the neighborhood',
            'hours': 5, 'date': 'Sun, Dec 3', 'time': '10AM-3PM',
            'location': 'Lawrenceville', 'mapX': 250, 'mapY': 220,
            'impact': 4, 'code': 'MURL', 'icon': 'palette'
        },
    ]
def saveEvents(events, filename='events.json'):
    """Save the current events list back to JSON so scraped + AI + organizer events persist."""
    with open(filename, 'w') as f:
        json.dump(events, f, indent=2)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def truncateText(text, maxChars):
    """Truncate text to fit within a maximum character count"""
    if len(text) <= maxChars:
        return text
    return text[:maxChars-2] + '..'

def getScale(app):
    """Get scale factor based on app size relative to base 400x700"""
    scaleX = app.width / 400
    scaleY = app.height / 700
    return min(scaleX, scaleY)

def getCenterX(app):
    """Get the center X position for content"""
    return app.width / 2

def getContentWidth(app):
    """Get the width of the content area (max 400, centered)"""
    return min(400, app.width - 40)

def getLeftMargin(app):
    """Get the left margin for centered content"""
    contentWidth = getContentWidth(app)
    return (app.width - contentWidth) / 2

# ============================================================================
# DRAWING FUNCTIONS
# ============================================================================

def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='white')

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
    elif app.mode == 'rewards':
        drawRewardsScreen(app)
    elif app.mode == 'eventDetail':
        drawEventDetailScreen(app)
    elif app.mode == 'verification':
        drawVerificationScreen(app)
    elif app.mode == 'orgDashboard':
        drawOrgDashboard(app)
    elif app.mode == 'orgEventDetail':
        drawOrgEventDetail(app)
    elif app.mode == 'createEvent':
        drawCreateEventScreen(app)

def drawIntroScreen(app):
    cx = getCenterX(app)
    contentW = getContentWidth(app)

    # Purple gradient header - original Givr theme
    headerH = app.height * 0.55
    drawRect(0, 0, app.width, headerH, fill=rgb(106, 90, 205))
    drawRect(0, 0, app.width, headerH * 0.5, fill=rgb(120, 105, 215))
    drawRect(0, 0, app.width, headerH * 0.2, fill=rgb(135, 120, 225))

    # Logo - clean heart shape with G
    logoY = headerH * 0.4
    s = 32  # scale for logo heart
    # Left bump
    drawCircle(cx - s * 0.45, logoY - s * 0.15, s * 0.52, fill='white')
    # Right bump
    drawCircle(cx + s * 0.45, logoY - s * 0.15, s * 0.52, fill='white')
    # Bottom point
    drawPolygon(cx - s * 0.88, logoY + s * 0.18,
                cx + s * 0.88, logoY + s * 0.18,
                cx, logoY + s * 1.0, fill='white')
    drawLabel('G', cx, logoY + 2, size=30, bold=True, fill=rgb(106, 90, 205), font='arial')

    # App name
    drawLabel('givr', cx, headerH - 55, size=48, bold=True, fill='white', font='arial')
    drawLabel('Swipe to give back', cx, headerH - 18, size=13, fill=rgb(200, 195, 240), font='arial')

    # White content area
    drawRect(0, headerH, app.width, app.height - headerH, fill='white')

    # Buttons
    btnY1 = headerH + 55
    btnY2 = headerH + 125
    btnW = min(280, contentW - 40)
    btnLeft = cx - btnW/2
    btnH = 50

    # CREATE ACCOUNT button - purple filled
    drawRect(btnLeft, btnY1, btnW, btnH, fill=rgb(106, 90, 205))
    drawLabel('CREATE ACCOUNT', cx, btnY1 + btnH/2, size=15, bold=True, fill='white', font='arial')

    # LOG IN button - outlined purple
    drawRect(btnLeft, btnY2, btnW, btnH, fill='white', border=rgb(106, 90, 205), borderWidth=2)
    drawLabel('LOG IN', cx, btnY2 + btnH/2, size=15, bold=True, fill=rgb(106, 90, 205), font='arial')

    # Footer
    drawLabel('Find meaningful volunteer opportunities', cx, app.height - 30, size=11, fill=rgb(150, 150, 150), font='arial')

def drawLoginScreen(app):
    cx = getCenterX(app)
    left = getLeftMargin(app)
    contentW = getContentWidth(app)
    fieldW = min(300, contentW - 20)
    fieldLeft = cx - fieldW/2

    # Header
    drawRect(0, 0, app.width, 100, fill='mediumSlateBlue')
    drawLabel('< Back', left + 20, 50, size=16, fill='white', align='left', font='monospace')
    drawLabel('Log In', cx, 50, size=24, bold=True, fill='white', font='monospace')

    # Login type toggle
    drawLabel('I am a:', cx, 130, size=14, fill='black', font='monospace')

    volActive = app.loginType == 'volunteer'
    orgActive = app.loginType == 'organizer'

    toggleW = min(145, (contentW - 30) / 2)
    drawRect(cx - toggleW - 5, 145, toggleW, 40, fill='mediumSlateBlue' if volActive else 'lightGray')
    drawLabel('Volunteer', cx - toggleW/2 - 5, 165, size=14, fill='white' if volActive else 'black', font='monospace')

    drawRect(cx + 5, 145, toggleW, 40, fill='darkSlateBlue' if orgActive else 'lightGray')
    drawLabel('Organizer', cx + toggleW/2 + 5, 165, size=14, fill='white' if orgActive else 'black', font='monospace')

    # Form
    drawLabel('Username', fieldLeft, 210, size=14, fill='gray', align='left', font='monospace')
    border = 'mediumSlateBlue' if app.activeField == 'username' else 'lightGray'
    drawRect(fieldLeft, 225, fieldW, 45, fill='white', border=border, borderWidth=2)
    text = truncateText(app.loginUsername if app.loginUsername else 'Enter username', 25)
    color = 'black' if app.loginUsername else 'lightGray'
    drawLabel(text, fieldLeft + 15, 247, size=16, fill=color, align='left', font='monospace')

    drawLabel('Password', fieldLeft, 290, size=14, fill='gray', align='left', font='monospace')
    border = 'mediumSlateBlue' if app.activeField == 'password' else 'lightGray'
    drawRect(fieldLeft, 305, fieldW, 45, fill='white', border=border, borderWidth=2)
    text = truncateText('*' * len(app.loginPassword) if app.loginPassword else 'Enter password', 25)
    color = 'black' if app.loginPassword else 'lightGray'
    drawLabel(text, fieldLeft + 15, 327, size=16, fill=color, align='left', font='monospace')

    if app.loginError:
        drawLabel(truncateText(app.loginError, 35), cx, 370, size=14, fill='red', font='monospace')

    # Login button
    btnColor = 'darkSlateBlue' if app.loginType == 'organizer' else 'mediumSlateBlue'
    drawRect(fieldLeft, 400, fieldW, 50, fill=btnColor)
    drawLabel('Log In', cx, 425, size=18, bold=True, fill='white', font='monospace')

    # Sign up link (only for volunteers)
    if app.loginType == 'volunteer':
        drawLabel("Don't have an account? Sign Up", cx, 480, size=14, fill='mediumSlateBlue', font='monospace')
    else:
        drawLabel('Organizer accounts pre-registered', cx, 480, size=12, fill='gray', font='monospace')

def drawSignupScreen(app):
    # Header
    drawRect(0, 0, app.width, 100, fill='mediumSlateBlue')
    drawLabel('< Back', 50, 50, size=16, fill='white', align='left', font='monospace')
    drawLabel('Sign Up', app.width/2, 50, size=24, bold=True, fill='white', font='monospace')

    # Signup type toggle
    drawLabel('I am a:', app.width/2, 125, size=14, fill='black', font='monospace')

    volActive = app.signupType == 'volunteer'
    orgActive = app.signupType == 'organizer'

    drawRect(50, 138, 145, 35, fill='mediumSlateBlue' if volActive else 'lightGray')
    drawLabel('Volunteer', 122, 155, size=13, fill='white' if volActive else 'black', font='monospace')

    drawRect(205, 138, 145, 35, fill='darkSlateBlue' if orgActive else 'lightGray')
    drawLabel('Organizer', 277, 155, size=13, fill='white' if orgActive else 'black', font='monospace')

    # Name field
    drawLabel('Name', 50, 190, size=14, fill='gray', align='left', font='monospace')
    border = 'mediumSlateBlue' if app.activeField == 'name' else 'lightGray'
    drawRect(50, 205, 300, 38, fill='white', border=border, borderWidth=2)
    text = app.signupName if app.signupName else 'Enter your name'
    color = 'black' if app.signupName else 'lightGray'
    drawLabel(text, 65, 224, size=14, fill=color, align='left', font='monospace')

    # Organization name field (only for organizers)
    if app.signupType == 'organizer':
        drawLabel('Organization Name', 50, 255, size=14, fill='gray', align='left', font='monospace')
        border = 'mediumSlateBlue' if app.activeField == 'orgname' else 'lightGray'
        drawRect(50, 270, 300, 38, fill='white', border=border, borderWidth=2)
        text = app.signupOrgName if app.signupOrgName else 'Enter organization name'
        color = 'black' if app.signupOrgName else 'lightGray'
        drawLabel(text, 65, 289, size=14, fill=color, align='left', font='monospace')
        yOffset = 65
    else:
        yOffset = 0

    # Username field
    drawLabel('Username', 50, 255 + yOffset, size=14, fill='gray', align='left', font='monospace')
    border = 'mediumSlateBlue' if app.activeField == 'username' else 'lightGray'
    drawRect(50, 270 + yOffset, 300, 38, fill='white', border=border, borderWidth=2)
    text = app.signupUsername if app.signupUsername else 'Choose username'
    color = 'black' if app.signupUsername else 'lightGray'
    drawLabel(text, 65, 289 + yOffset, size=14, fill=color, align='left', font='monospace')

    # Password field
    drawLabel('Password', 50, 320 + yOffset, size=14, fill='gray', align='left', font='monospace')
    border = 'mediumSlateBlue' if app.activeField == 'password' else 'lightGray'
    drawRect(50, 335 + yOffset, 300, 38, fill='white', border=border, borderWidth=2)
    text = '*' * len(app.signupPassword) if app.signupPassword else 'Create password'
    color = 'black' if app.signupPassword else 'lightGray'
    drawLabel(text, 65, 354 + yOffset, size=14, fill=color, align='left', font='monospace')

    if app.signupError:
        drawLabel(app.signupError, app.width/2, 390 + yOffset, size=14, fill='red', font='monospace')

    # Signup button
    btnColor = 'darkSlateBlue' if app.signupType == 'organizer' else 'mediumSlateBlue'
    drawRect(50, 420 + yOffset, 300, 50, fill=btnColor)
    drawLabel('Create Account', app.width/2, 445 + yOffset, size=18, bold=True, fill='white', font='monospace')

    drawLabel('Already have an account? Log In', app.width/2, 500 + yOffset, size=14, fill='mediumSlateBlue', font='monospace')

def drawPreferencesScreen(app):
    # Header
    drawRect(0, 0, app.width, 80, fill='mediumSlateBlue')
    drawLabel('Your Preferences', app.width/2, 45, size=22, bold=True, fill='white', font='monospace')

    # Categories
    drawLabel('Select causes you care about:', 30, 110, size=14, fill='black', align='left', font='monospace')

    for i, cat in enumerate(app.categories):
        row = i // 2
        col = i % 2
        x = 30 + col * 175
        y = 140 + row * 50

        isSelected = cat in app.selectedCategories
        bgColor = app.categoryColors[cat] if isSelected else 'lightGray'
        textColor = 'white' if isSelected else 'black'

        drawRect(x, y, 160, 40, fill=bgColor)
        drawLabel(cat, x + 80, y + 20, size=14, fill=textColor, bold=isSelected, font='monospace')

    # Time preference
    drawLabel('When are you available?', 30, 310, size=14, fill='black', align='left', font='monospace')

    times = [('weekdays', 'Weekdays'), ('weekends', 'Weekends'), ('either', 'Either')]
    for i, (val, label) in enumerate(times):
        x = 30 + i * 120
        isSelected = app.timePreference == val
        bgColor = 'mediumSlateBlue' if isSelected else 'lightGray'
        textColor = 'white' if isSelected else 'black'

        drawRect(x, 340, 110, 40, fill=bgColor)
        drawLabel(label, x + 55, 360, size=13, fill=textColor, font='monospace')

    # Experience
    drawLabel('Experience level:', 30, 410, size=14, fill='black', align='left', font='monospace')

    exps = [('new', 'New'), ('experienced', 'Experienced')]
    for i, (val, label) in enumerate(exps):
        x = 30 + i * 175
        isSelected = app.experienceLevel == val
        bgColor = 'slateBlue' if isSelected else 'lightGray'
        textColor = 'white' if isSelected else 'black'

        drawRect(x, 440, 160, 40, fill=bgColor)
        drawLabel(label, x + 80, 460, size=14, fill=textColor, font='monospace')

    # Continue button
    canContinue = len(app.selectedCategories) > 0 and app.timePreference
    bgColor = 'mediumSlateBlue' if canContinue else 'lightGray'
    drawRect(50, 520, 300, 50, fill=bgColor)
    drawLabel('Start Swiping', app.width/2, 545, size=18, bold=True, fill='white', font='monospace')

    drawLabel('Skip for now', app.width/2, 600, size=14, fill='gray', font='monospace')

def drawSwipeScreen(app):
    cx = getCenterX(app)
    left = getLeftMargin(app)
    contentW = getContentWidth(app)

    # Clean white header
    drawRect(0, 0, app.width, 60, fill='white')
    drawRect(0, 58, app.width, 1, fill=rgb(240, 240, 240))

    # Logo - purple theme
    drawLabel('givr', cx, 32, size=26, bold=True, fill=rgb(106, 90, 205), font='arial')

    # User avatar (top right)
    if app.currentUser and app.currentUser in app.users:
        userName = app.users[app.currentUser].get('name', '')
        drawUserAvatar(app.width - left - 25, 30, 16, userName)

    # Calculate card dimensions - taller like Tinder
    cardW = min(340, contentW - 20)
    cardH = min(480, app.height - 160)
    cardX = cx - cardW/2 + app.cardOffsetX
    cardY = 70

    # Button positions
    btnY = min(app.height - 75, cardY + cardH + 20)
    skipBtnX = cx - 80
    saveBtnX = cx + 80

    if app.currentEventIndex >= len(app.events):
        # Empty state
        drawLabel('No more events', cx, app.height/2 - 20, size=24, bold=True, fill=rgb(80, 80, 80), font='arial')
        drawLabel('Check back later for more opportunities', cx, app.height/2 + 15, size=13, fill=rgb(150, 150, 150), font='arial')

        btnW = min(200, contentW - 60)
        drawRect(cx - btnW/2, app.height/2 + 50, btnW, 45, fill=rgb(106, 90, 205))
        drawLabel('BROWSE ALL', cx, app.height/2 + 73, size=14, bold=True, fill='white', font='arial')
    else:
        # Draw Tinder-style card
        event = app.events[app.currentEventIndex]
        drawTinderCard(app, event, cardX, cardY, cardW, cardH)

        # Swipe indicators
        if app.cardOffsetX > 40:
            drawLabel('LIKE', cardX + 50, cardY + 50, size=32, bold=True, fill=rgb(30, 200, 80), font='arial', rotateAngle=-15)
        elif app.cardOffsetX < -40:
            drawLabel('NOPE', cardX + cardW - 60, cardY + 50, size=32, bold=True, fill=rgb(255, 80, 80), font='arial', rotateAngle=15)

        # Action buttons - Tinder style (larger, cleaner)
        # X button (skip)
        drawCircle(skipBtnX, btnY, 30, fill='white', border=rgb(255, 180, 180), borderWidth=2)
        drawTinderX(skipBtnX, btnY, 32)

        # Heart button (save)
        drawCircle(saveBtnX, btnY, 30, fill='white', border=rgb(180, 255, 180), borderWidth=2)
        drawTinderHeart(saveBtnX, btnY, 32)

        # Card counter
        drawLabel(f'{app.currentEventIndex + 1} / {len(app.events)}', cx, btnY, size=12, fill=rgb(150, 150, 150), font='arial')

    drawNavBar(app, 0)

def drawTinderCard(app, event, x, y, cardW=350, cardH=450):
    """Draw a clean Tinder-style card"""
    iconType = event.get('icon', 'heart')

    # Category colors
    catColors = {
        'Environment': rgb(76, 175, 80),
        'Education': rgb(33, 150, 243),
        'Community': rgb(255, 152, 0),
        'Health': rgb(233, 30, 99),
        'Arts': rgb(156, 39, 176)
    }
    mainColor = catColors.get(event['category'], rgb(158, 158, 158))

    # Card shadow
    drawRect(x + 4, y + 4, cardW, cardH, fill=rgb(210, 210, 210))

    # Card background
    drawRect(x, y, cardW, cardH, fill='white', border=rgb(235, 235, 235), borderWidth=1)

    # Image/icon area - clean gradient
    imageH = cardH * 0.45
    drawRect(x, y, cardW, imageH, fill=mainColor)

    # Draw the event icon centered
    iconCx = x + cardW / 2
    iconCy = y + imageH / 2
    drawEventIcon(iconType, iconCx, iconCy, 75)

    # Category tag (top left) - clean pill
    catPillW = len(event['category']) * 7 + 20
    drawRect(x + 15, y + 15, catPillW, 26, fill='white')
    drawLabel(event['category'], x + 15 + catPillW/2, y + 28, size=11, bold=True, fill=mainColor, font='arial')

    # Hours badge (top right)
    drawRect(x + cardW - 55, y + 15, 40, 26, fill='white')
    drawLabel(f"{event['hours']}h", x + cardW - 35, y + 28, size=12, bold=True, fill=mainColor, font='arial')

    # Content area below image
    contentY = y + imageH + 18

    # Title - clean, bold
    maxTitleChars = int(cardW / 10)
    drawLabel(truncateText(event['title'], maxTitleChars), x + cardW/2, contentY,
              size=20, bold=True, fill=rgb(30, 30, 30), font='arial')

    # Organization
    drawLabel(truncateText(event['org'], 30), x + cardW/2, contentY + 26,
              size=12, fill=rgb(130, 130, 130), font='arial')

    # Divider
    drawLine(x + 20, contentY + 48, x + cardW - 20, contentY + 48, fill=rgb(240, 240, 240), lineWidth=1)

    # Description
    descY = contentY + 68
    maxDescChars = int(cardW / 7)
    drawLabel(truncateText(event['desc'], maxDescChars), x + cardW/2, descY,
              size=11, fill=rgb(100, 100, 100), font='arial')

    # Details section - clean list style
    detailY = descY + 30
    detailSpacing = 22

    # Date
    drawLabel('Date:', x + 20, detailY, size=10, fill=rgb(150, 150, 150), align='left', font='arial')
    drawLabel(event['date'], x + 70, detailY, size=11, fill=rgb(60, 60, 60), align='left', font='arial')

    # Time
    drawLabel('Time:', x + 20, detailY + detailSpacing, size=10, fill=rgb(150, 150, 150), align='left', font='arial')
    drawLabel(event['time'], x + 70, detailY + detailSpacing, size=11, fill=rgb(60, 60, 60), align='left', font='arial')

    # Location
    drawLabel('Where:', x + 20, detailY + detailSpacing * 2, size=10, fill=rgb(150, 150, 150), align='left', font='arial')
    drawLabel(event['location'], x + 75, detailY + detailSpacing * 2, size=11, fill=rgb(60, 60, 60), align='left', font='arial')

    # Impact stars at bottom
    impactY = y + cardH - 22
    drawLabel('Impact:', x + 20, impactY, size=10, fill=rgb(150, 150, 150), align='left', font='arial')
    for i in range(5):
        starColor = rgb(255, 190, 50) if i < event['impact'] else rgb(220, 220, 220)
        drawStar(x + 80 + i * 18, impactY, 8, starColor)

def drawEventCard(app, event, x, y, cardW=340, cardH=420):
    """Legacy card drawing function for list views"""
    # Card shadow
    drawRect(x + 3, y + 3, cardW, cardH, fill='lightGray')
    # Card
    drawRect(x, y, cardW, cardH, fill='white', border='lightGray', borderWidth=1)

    # Category banner
    catColor = app.categoryColors.get(event['category'], 'gray')
    drawRect(x, y, cardW, 50, fill=catColor)
    drawLabel(truncateText(event['category'], 12), x + 15, y + 25, size=14, fill='white', align='left', bold=True, font='monospace')
    drawLabel(f"{event['hours']}h", x + cardW - 40, y + 25, size=14, fill='white', bold=True, font='monospace')

    # Title and org - truncate based on card width
    maxTitleChars = int(cardW / 12)
    maxOrgChars = int(cardW / 10)
    drawLabel(truncateText(event['title'], maxTitleChars), x + cardW/2, y + 85, size=20, bold=True, fill='black', font='monospace')
    drawLabel(truncateText(event['org'], maxOrgChars), x + cardW/2, y + 115, size=13, fill='gray', font='monospace')

    # Line
    drawLine(x + 20, y + 140, x + cardW - 20, y + 140, fill='lightGray')

    # Description - truncate based on card width
    maxDescChars = int(cardW / 8)
    drawLabel(truncateText(event['desc'], maxDescChars), x + cardW/2, y + 170, size=13, fill='black', font='monospace')

    # Details - with value column that fits
    labelX = x + 25
    valueX = x + 85
    maxValueChars = int((cardW - 100) / 8)

    drawLabel('Date:', labelX, y + 210, size=11, fill='gray', align='left', font='monospace')
    drawLabel(truncateText(event['date'], maxValueChars), valueX, y + 210, size=11, fill='black', align='left', font='monospace')

    drawLabel('Time:', labelX, y + 240, size=11, fill='gray', align='left', font='monospace')
    drawLabel(truncateText(event['time'], maxValueChars), valueX, y + 240, size=11, fill='black', align='left', font='monospace')

    drawLabel('Where:', labelX, y + 270, size=11, fill='gray', align='left', font='monospace')
    drawLabel(truncateText(event['location'], maxValueChars), valueX, y + 270, size=11, fill='black', align='left', font='monospace')

    # Impact
    drawLabel('Impact:', labelX, y + 310, size=11, fill='gray', align='left', font='monospace')
    starSize = min(10, cardW / 40)
    starSpacing = min(25, cardW / 15)
    for i in range(5):
        starColor = 'gold' if i < event['impact'] else 'lightGray'
        drawStar(valueX + i * starSpacing, y + 310, starSize, starColor)

def drawAllEventsScreen(app):
    drawRect(0, 0, app.width, 60, fill='white', border='lightGray', borderWidth=1)
    drawLabel('All Events', app.width/2, 35, size=20, bold=True, fill='black', font='monospace')

    # Logout button
    drawRect(app.width - 70, 20, 55, 30, fill='lightGray')
    drawLabel('Logout', app.width - 42, 35, size=10, fill='gray', font='monospace')

    # Event list
    for i, event in enumerate(app.events[:5]):
        y = 80 + i * 90
        drawEventListItem(app, event, 20, y)

    drawNavBar(app, 1)

def drawEventListItem(app, event, x, y):
    # Card
    drawRect(x, y, 360, 80, fill='white', border='lightGray', borderWidth=1)

    # Category indicator
    catColor = app.categoryColors.get(event['category'], 'gray')
    drawRect(x, y, 6, 80, fill=catColor)

    # Content
    drawLabel(event['title'], x + 20, y + 20, size=15, bold=True, fill='black', align='left', font='monospace')
    drawLabel(event['org'], x + 20, y + 42, size=12, fill='gray', align='left', font='monospace')
    drawLabel(f"{event['date']} | {event['hours']}h | {event['location']}",
              x + 20, y + 62, size=11, fill='gray', align='left')

    # Save button
    isSaved = event in app.savedEvents
    color = 'green' if isSaved else 'lightGray'
    drawCircle(x + 330, y + 40, 18, fill=color)
    drawLabel('+', x + 330, y + 40, size=20, fill='white', bold=True, font='monospace')

def drawSavedScreen(app):
    drawRect(0, 0, app.width, 60, fill='white', border='lightGray', borderWidth=1)
    drawLabel('Saved Events', app.width/2, 35, size=20, bold=True, fill='black', font='monospace')

    # Logout button
    drawRect(app.width - 70, 20, 55, 30, fill='lightGray')
    drawLabel('Logout', app.width - 42, 35, size=10, fill='gray', font='monospace')

    if len(app.savedEvents) == 0:
        drawLabel('No saved events', app.width/2, 300, size=18, fill='gray', font='monospace')
        drawLabel('Swipe right to save events!', app.width/2, 330, size=14, fill='lightGray', font='monospace')
    else:
        for i, event in enumerate(app.savedEvents[:4]):
            y = 80 + i * 110
            drawSavedEventItem(app, event, 20, y)

    drawNavBar(app, 2)  # Saved is now index 2

def drawSavedEventItem(app, event, x, y):
    drawRect(x, y, 360, 100, fill='white', border='lightGray', borderWidth=1)

    # Category bar
    catColor = app.categoryColors.get(event['category'], 'gray')
    drawRect(x, y, 6, 100, fill=catColor)

    # Status
    isVerified = event in app.verifiedEvents
    isCompleted = event in app.completedEvents

    if isVerified:
        statusColor = 'green'
        statusText = 'Verified'
    elif isCompleted:
        statusColor = 'orange'
        statusText = 'Pending'
    else:
        statusColor = 'gray'
        statusText = 'Upcoming'

    drawRect(x + 270, y + 10, 80, 24, fill=statusColor)
    drawLabel(statusText, x + 310, y + 22, size=11, fill='white', bold=True, font='monospace')

    # Content
    drawLabel(event['title'], x + 20, y + 25, size=15, bold=True, fill='black', align='left', font='monospace')
    drawLabel(event['org'], x + 20, y + 47, size=12, fill='gray', align='left', font='monospace')
    drawLabel(f"{event['date']} | {event['hours']}h", x + 20, y + 67, size=11, fill='gray', align='left', font='monospace')

    # Action button
    if not isVerified:
        btnText = 'Verify' if isCompleted else 'Complete'
        drawRect(x + 260, y + 65, 90, 28, fill='mediumSlateBlue')
        drawLabel(btnText, x + 305, y + 79, size=12, fill='white', bold=True, font='monospace')

def drawRewardsScreen(app):
    drawRect(0, 0, app.width, 100, fill='mediumSlateBlue')
    drawLabel('Your Impact', app.width/2, 55, size=22, bold=True, fill='white', font='monospace')

    # Logout button
    drawRect(app.width - 70, 20, 55, 30, fill='white')
    drawLabel('Logout', app.width - 42, 35, size=10, fill='mediumSlateBlue', font='monospace')

    # Stats
    drawRect(20, 120, 170, 70, fill='white', border='lightGray', borderWidth=1)
    drawLabel(str(app.totalHours), 105, 145, size=28, bold=True, fill='mediumSlateBlue', font='monospace')
    drawLabel('Hours', 105, 175, size=12, fill='gray', font='monospace')

    drawRect(210, 120, 170, 70, fill='white', border='lightGray', borderWidth=1)
    drawLabel(str(app.totalPoints), 295, 145, size=28, bold=True, fill='slateBlue', font='monospace')
    drawLabel('Points', 295, 175, size=12, fill='gray', font='monospace')

    # Tier
    tierName = app.tierNames[app.currentTier - 1]
    drawRect(20, 210, 360, 70, fill='white', border='lightGray', borderWidth=1)
    drawLabel(f'Tier {app.currentTier}: {tierName}', app.width/2, 235, size=16, bold=True, fill='black', font='monospace')

    # Progress bar
    if app.currentTier < 4:
        nextThreshold = app.tierThresholds[app.currentTier]
        progress = min(1, app.totalPoints / nextThreshold) if nextThreshold > 0 else 0
        drawRect(40, 260, 320, 12, fill='lightGray')
        if progress > 0:
            drawRect(40, 260, 320 * progress, 12, fill='mediumSlateBlue')

    # Streak
    drawRect(20, 300, 360, 50, fill='white', border='lightGray', borderWidth=1)
    drawLabel('Weekly Streak:', 100, 325, size=14, fill='black', align='left', font='monospace')
    drawLabel(f'{app.weeklyStreak} weeks', 320, 325, size=16, bold=True, fill='orange', font='monospace')

    # Badges section
    drawLabel('Badges', 30, 370, size=16, bold=True, fill='black', align='left', font='monospace')

    badgeList = list(app.badges.items())
    for i, (key, badge) in enumerate(badgeList):
        x = 50 + (i % 4) * 85
        y = 430 + (i // 4) * 80

        color = 'gold' if badge['unlocked'] else 'lightGray'
        drawCircle(x, y, 25, fill=color)
        drawLabel('?' if not badge['unlocked'] else 'B', x, y, size=16, fill='white', bold=True, font='monospace')
        drawLabel(badge['name'], x, y - 40, size=9, fill='gray', font='monospace')  # Name above circle

    drawNavBar(app, 3)  # Rewards is now index 3

def wrapText(text, maxCharsPerLine):
    """Wrap text into multiple lines"""
    words = text.split(' ')
    lines = []
    currentLine = ''

    for word in words:
        if len(currentLine) + len(word) + 1 <= maxCharsPerLine:
            if currentLine:
                currentLine += ' ' + word
            else:
                currentLine = word
        else:
            if currentLine:
                lines.append(currentLine)
            currentLine = word

    if currentLine:
        lines.append(currentLine)

    return lines

def drawEventDetailScreen(app):
    if not app.selectedEvent:
        return

    event = app.selectedEvent
    catColor = app.categoryColors.get(event['category'], 'gray')
    primaryPurple = rgb(106, 90, 205)
    lightPurple = rgb(230, 225, 250)

    # Full background
    drawRect(0, 0, app.width, app.height, fill=rgb(245, 245, 250))

    # Header with gradient effect (two overlapping rects)
    drawRect(0, 0, app.width, 160, fill=primaryPurple)
    drawRect(0, 130, app.width, 50, fill=rgb(245, 245, 250))

    # Back button with circle background
    drawCircle(45, 50, 20, fill=rgb(255, 255, 255))
    drawLabel('<', 45, 50, size=20, fill=primaryPurple, bold=True)

    # Category pill
    catWidth = len(event['category']) * 9 + 24
    drawRect(app.width/2 - catWidth/2, 30, catWidth, 26, fill=rgb(255, 255, 255))
    drawLabel(event['category'].upper(), app.width/2, 43, size=11, fill=primaryPurple, bold=True, font='monospace')

    # Event title (truncated if needed)
    titleText = truncateText(event['title'], 28)
    drawLabel(titleText, app.width/2, 85, size=20, bold=True, fill='white', font='monospace')

    # Organization name
    drawLabel(event['org'], app.width/2, 112, size=13, fill=rgb(200, 195, 230), font='monospace')

    # Main content card with shadow effect
    cardX = 20
    cardY = 145
    cardWidth = app.width - 40
    cardHeight = 380

    # Shadow
    drawRect(cardX + 3, cardY + 3, cardWidth, cardHeight, fill=rgb(200, 200, 210))
    # Card
    drawRect(cardX, cardY, cardWidth, cardHeight, fill='white', border=rgb(230, 230, 240), borderWidth=1)

    # About section with icon
    drawCircle(50, 175, 14, fill=lightPurple)
    drawLabel('i', 50, 175, size=14, fill=primaryPurple, bold=True)
    drawLabel('About', 75, 175, size=14, bold=True, fill=rgb(50, 50, 60), align='left', font='monospace')

    # Wrap description text properly
    descLines = wrapText(event['desc'], 38)
    for i, line in enumerate(descLines[:3]):  # Max 3 lines
        drawLabel(line, 40, 205 + i * 20, size=12, fill=rgb(100, 100, 110), align='left', font='monospace')

    # Divider
    drawLine(40, 275, app.width - 60, 275, fill=rgb(230, 230, 240), lineWidth=1)

    # Details section with icons
    details = [
        ('calendar', 'Date', event['date']),
        ('clock', 'Time', event['time']),
        ('pin', 'Location', truncateText(event['location'], 22)),
        ('hourglass', 'Hours', str(event['hours']) + ' volunteer hours')
    ]

    for i, (icon, label, value) in enumerate(details):
        y = 305 + i * 45

        # Icon circle
        drawCircle(50, y, 14, fill=lightPurple)

        # Icon symbols
        if icon == 'calendar':
            drawRect(44, y - 6, 12, 10, fill=primaryPurple)
            drawRect(46, y - 4, 8, 6, fill='white')
        elif icon == 'clock':
            drawCircle(50, y, 8, fill=None, border=primaryPurple, borderWidth=2)
            drawLine(50, y, 50, y - 4, fill=primaryPurple, lineWidth=2)
            drawLine(50, y, 54, y, fill=primaryPurple, lineWidth=2)
        elif icon == 'pin':
            drawCircle(50, y - 2, 5, fill=primaryPurple)
            drawPolygon(45, y, 55, y, 50, y + 7, fill=primaryPurple)
        elif icon == 'hourglass':
            drawPolygon(45, y - 6, 55, y - 6, 50, y, fill=primaryPurple)
            drawPolygon(45, y + 6, 55, y + 6, 50, y, fill=primaryPurple)

        drawLabel(label, 75, y - 6, size=11, fill=rgb(150, 150, 160), align='left', font='monospace')
        drawLabel(value, 75, y + 10, size=13, fill=rgb(50, 50, 60), align='left', bold=True, font='monospace')

    # Impact section
    drawLine(40, 480, app.width - 60, 480, fill=rgb(230, 230, 240), lineWidth=1)
    drawLabel('Impact Level', 40, 505, size=12, fill=rgb(100, 100, 110), align='left', font='monospace')

    # Stars with better styling
    for i in range(5):
        x = app.width - 60 - (4 - i) * 28
        if i < event['impact']:
            drawStar(x, 505, 10, 'gold')
        else:
            drawStar(x, 505, 10, rgb(220, 220, 230))

    # Save button with shadow and better styling
    isSaved = event in app.savedEvents
    btnY = 545
    btnHeight = 52

    # Button shadow
    drawRect(35, btnY + 3, app.width - 70, btnHeight, fill=rgb(180, 180, 190))

    if isSaved:
        # Saved state - green with checkmark
        drawRect(32, btnY, app.width - 64, btnHeight, fill=rgb(50, 200, 100))
        drawLabel('Saved!', app.width/2, btnY + btnHeight/2, size=18, bold=True, fill='white', font='monospace')
    else:
        # Save state - purple gradient effect
        drawRect(32, btnY, app.width - 64, btnHeight, fill=primaryPurple)
        drawLabel('Save Event', app.width/2 + 10, btnY + btnHeight/2, size=18, bold=True, fill='white', font='monospace')
        # Heart icon
        heartX = app.width/2 - 55
        heartY = btnY + btnHeight/2
        s = 8
        drawCircle(heartX - s * 0.4, heartY - s * 0.1, s * 0.5, fill='white')
        drawCircle(heartX + s * 0.4, heartY - s * 0.1, s * 0.5, fill='white')
        drawPolygon(heartX - s * 0.8, heartY + s * 0.2, heartX + s * 0.8, heartY + s * 0.2, heartX, heartY + s * 0.9, fill='white')

def drawVerificationScreen(app):
    # Overlay
    drawRect(0, 0, app.width, app.height, fill='gray')

    # Modal
    drawRect(40, 200, 320, 280, fill='white', border='lightGray', borderWidth=1)

    # Close button
    drawCircle(340, 220, 15, fill='lightGray')
    drawLabel('X', 340, 220, size=14, fill='gray', bold=True, font='monospace')

    drawLabel('Verify Attendance', app.width/2, 250, size=20, bold=True, fill='black', font='monospace')

    if app.verificationEvent:
        drawLabel(app.verificationEvent['title'], app.width/2, 280, size=14, fill='gray', font='monospace')

    drawLabel('Enter the 4-character code:', app.width/2, 320, size=13, fill='black', font='monospace')

    # Code boxes
    for i in range(4):
        x = 100 + i * 55
        drawRect(x, 350, 45, 50, fill='white', border='mediumSlateBlue', borderWidth=2)
        if i < len(app.verificationCode):
            drawLabel(app.verificationCode[i].upper(), x + 22, 375, size=24, bold=True, fill='black')

    if app.verificationError:
        drawLabel(app.verificationError, app.width/2, 420, size=13, fill='red', font='monospace')

    # Verify button
    canVerify = len(app.verificationCode) == 4
    btnColor = 'mediumSlateBlue' if canVerify else 'lightGray'
    drawRect(80, 440, 240, 40, fill=btnColor)
    drawLabel('Verify', app.width/2, 460, size=16, bold=True, fill='white', font='monospace')

def drawOrgDashboard(app):
    # Header
    drawRect(0, 0, app.width, 100, fill='darkSlateBlue')
    drawLabel('Organizer Dashboard', app.width/2, 40, size=20, bold=True, fill='white', font='monospace')

    if app.currentUser and app.currentUser in app.organizers:
        orgName = app.organizers[app.currentUser]['name']
        drawLabel(orgName, app.width/2, 70, size=14, fill='white', font='monospace')

    # Logout button
    drawRect(app.width - 80, 30, 60, 30, fill='white')
    drawLabel('Logout', app.width - 50, 45, size=11, fill='darkSlateBlue', font='monospace')

    # Instructions
    drawRect(20, 120, 360, 60, fill='lavender', border='darkSlateBlue', borderWidth=1)
    drawLabel('Tap an event to view its verification code', app.width/2, 140, size=13, fill='darkSlateBlue', font='monospace')
    drawLabel('Share this code with volunteers who attend', app.width/2, 160, size=12, fill='gray', font='monospace')

    # Create Event button
    drawRect(20, 200, 360, 45, fill='green')
    drawLabel('+ Create New Event', app.width/2, 222, size=16, bold=True, fill='white', font='monospace')

    # Get organizer's events
    orgEvents = getOrganizerEvents(app)

    drawLabel('Your Events', 30, 270, size=16, bold=True, fill='black', align='left', font='monospace')

    if len(orgEvents) == 0:
        drawLabel('No events found', app.width/2, 360, size=16, fill='gray', font='monospace')
    else:
        for i, event in enumerate(orgEvents[:4]):
            y = 300 + i * 85
            drawOrgEventItem(app, event, 20, y)

def drawOrgEventItem(app, event, x, y):
    # Card
    drawRect(x, y, 360, 75, fill='white', border='lightGray', borderWidth=1)

    # Category indicator
    catColor = app.categoryColors.get(event['category'], 'gray')
    drawRect(x, y, 6, 75, fill=catColor)

    # Content
    drawLabel(event['title'], x + 20, y + 20, size=15, bold=True, fill='black', align='left', font='monospace')
    drawLabel(f"{event['date']} | {event['time']}", x + 20, y + 42, size=12, fill='gray', align='left', font='monospace')

    # Code preview (hidden)
    drawRect(x + 270, y + 15, 80, 45, fill='darkSlateBlue')
    drawLabel('VIEW', x + 310, y + 30, size=10, fill='white', font='monospace')
    drawLabel('CODE', x + 310, y + 45, size=10, fill='white', font='monospace')

def drawOrgEventDetail(app):
    if not app.selectedOrgEvent:
        return

    event = app.selectedOrgEvent
    catColor = app.categoryColors.get(event['category'], 'gray')

    # Header
    drawRect(0, 0, app.width, 120, fill='darkSlateBlue')
    drawLabel('< Back', 40, 40, size=16, fill='white', align='left', font='monospace')
    drawLabel('Event Details', app.width/2, 40, size=18, bold=True, fill='white', font='monospace')
    drawLabel(event['title'], app.width/2, 80, size=20, bold=True, fill='white', font='monospace')
    drawLabel(event['org'], app.width/2, 105, size=14, fill='white', font='monospace')

    # Event info card
    drawRect(20, 140, 360, 150, fill='white', border='lightGray', borderWidth=1)

    drawLabel('Event Information', 40, 165, size=14, bold=True, fill='black', align='left', font='monospace')

    details = [
        ('Category', event['category']),
        ('Date', event['date']),
        ('Time', event['time']),
        ('Location', event['location']),
    ]

    for i, (label, value) in enumerate(details):
        y = 195 + i * 25
        drawLabel(label + ':', 40, y, size=12, fill='gray', align='left', font='monospace')
        drawLabel(value, 360, y, size=12, fill='black', align='right', font='monospace')

    # Verification code card
    drawRect(20, 310, 360, 180, fill='lavender', border='darkSlateBlue', borderWidth=2)

    drawLabel('VERIFICATION CODE', app.width/2, 340, size=14, bold=True, fill='darkSlateBlue', font='monospace')
    drawLabel('Share this code with volunteers', app.width/2, 365, size=12, fill='gray', font='monospace')

    # Big code display
    drawRect(80, 390, 240, 70, fill='white', border='darkSlateBlue', borderWidth=3)
    drawLabel(event['code'], app.width/2, 425, size=40, bold=True, fill='darkSlateBlue', font='monospace')

    # Stats
    drawRect(20, 510, 360, 80, fill='white', border='lightGray', borderWidth=1)
    drawLabel('Event Stats', 40, 535, size=14, bold=True, fill='black', align='left', font='monospace')

    # Count verified volunteers
    verifiedCount = sum(1 for e in app.verifiedEvents if e['id'] == event['id'])
    drawLabel(f'Verified Volunteers: {verifiedCount}', 40, 565, size=13, fill='gray', align='left', font='monospace')

def drawCreateEventScreen(app):
    # Header
    drawRect(0, 0, app.width, 80, fill='darkSlateBlue')
    drawLabel('< Back', 40, 45, size=16, fill='white', align='left', font='monospace')
    drawLabel('Create Event', app.width/2, 45, size=20, bold=True, fill='white', font='monospace')

    # Title field
    drawLabel('Title', 30, 105, size=12, fill='gray', align='left', font='monospace')
    border = 'darkSlateBlue' if app.createEventField == 'title' else 'lightGray'
    drawRect(30, 118, 340, 35, fill='white', border=border, borderWidth=2)
    text = app.newEventTitle if app.newEventTitle else 'Event title'
    color = 'black' if app.newEventTitle else 'lightGray'
    drawLabel(text, 40, 135, size=13, fill=color, align='left', font='monospace')

    # Description field
    drawLabel('Description', 30, 165, size=12, fill='gray', align='left', font='monospace')
    border = 'darkSlateBlue' if app.createEventField == 'desc' else 'lightGray'
    drawRect(30, 178, 340, 35, fill='white', border=border, borderWidth=2)
    text = app.newEventDesc if app.newEventDesc else 'Brief description'
    color = 'black' if app.newEventDesc else 'lightGray'
    drawLabel(text, 40, 195, size=13, fill=color, align='left', font='monospace')

    # Date and Time row
    drawLabel('Date', 30, 225, size=12, fill='gray', align='left', font='monospace')
    border = 'darkSlateBlue' if app.createEventField == 'date' else 'lightGray'
    drawRect(30, 238, 160, 35, fill='white', border=border, borderWidth=2)
    text = app.newEventDate if app.newEventDate else 'e.g. Sat, Dec 7'
    color = 'black' if app.newEventDate else 'lightGray'
    drawLabel(text, 40, 255, size=11, fill=color, align='left', font='monospace')

    drawLabel('Time', 210, 225, size=12, fill='gray', align='left', font='monospace')
    border = 'darkSlateBlue' if app.createEventField == 'time' else 'lightGray'
    drawRect(210, 238, 160, 35, fill='white', border=border, borderWidth=2)
    text = app.newEventTime if app.newEventTime else 'e.g. 10AM-1PM'
    color = 'black' if app.newEventTime else 'lightGray'
    drawLabel(text, 220, 255, size=11, fill=color, align='left', font='monospace')

    # Location and Hours row
    drawLabel('Location', 30, 285, size=12, fill='gray', align='left', font='monospace')
    border = 'darkSlateBlue' if app.createEventField == 'location' else 'lightGray'
    drawRect(30, 298, 160, 35, fill='white', border=border, borderWidth=2)
    text = app.newEventLocation if app.newEventLocation else 'Neighborhood'
    color = 'black' if app.newEventLocation else 'lightGray'
    drawLabel(text, 40, 315, size=11, fill=color, align='left', font='monospace')

    drawLabel('Hours', 210, 285, size=12, fill='gray', align='left', font='monospace')
    border = 'darkSlateBlue' if app.createEventField == 'hours' else 'lightGray'
    drawRect(210, 298, 160, 35, fill='white', border=border, borderWidth=2)
    text = app.newEventHours if app.newEventHours else 'e.g. 3'
    color = 'black' if app.newEventHours else 'lightGray'
    drawLabel(text, 220, 315, size=11, fill=color, align='left', font='monospace')

    # Category selection
    drawLabel('Category', 30, 345, size=12, fill='gray', align='left', font='monospace')
    for i, cat in enumerate(app.categories):
        x = 30 + (i % 3) * 115
        y = 360 + (i // 3) * 35
        isSelected = app.newEventCategory == cat
        bgColor = app.categoryColors[cat] if isSelected else 'lightGray'
        drawRect(x, y, 105, 28, fill=bgColor)
        drawLabel(cat, x + 52, y + 14, size=10, fill='white' if isSelected else 'black', font='monospace')

    # Impact selection
    drawLabel('Impact (1-5):', 30, 440, size=12, fill='gray', align='left')
    for i in range(5):
        starColor = 'gold' if i < app.newEventImpact else 'lightGray'
        drawStar(140 + i * 30, 440, 12, starColor)

    if app.createEventError:
        drawLabel(app.createEventError, app.width/2, 480, size=12, fill='red', font='monospace')

    # Create button
    drawRect(30, 500, 340, 50, fill='darkSlateBlue')
    drawLabel('Create Event', app.width/2, 525, size=18, bold=True, fill='white', font='monospace')

def getOrganizerEvents(app):
    """Get events belonging to the current organizer"""
    if not app.currentUser or app.currentUser not in app.organizers:
        return []

    orgName = app.organizers[app.currentUser]['org']
    return [e for e in app.events if e['org'] == orgName]

def drawNavBar(app, activeIndex):
    y = app.height - 55
    # Clean nav bar
    drawRect(0, y, app.width, 55, fill='white')
    drawRect(0, y, app.width, 1, fill=rgb(235, 235, 235))

    tabs = ['Swipe', 'Browse', 'Saved', 'Profile']
    tabWidth = app.width / 4

    for i, tab in enumerate(tabs):
        tx = i * tabWidth + tabWidth / 2
        isActive = i == activeIndex
        color = rgb(106, 90, 205) if isActive else rgb(180, 180, 180)

        # Tab label
        drawLabel(tab, tx, y + 30, size=11, fill=color, bold=isActive, font='arial')

        # Active indicator
        if isActive:
            drawRect(tx - 20, y + 2, 40, 3, fill=rgb(106, 90, 205))

def drawStar(cx, cy, size, color):
    points = []
    for i in range(10):
        angle = math.radians(i * 36 - 90)
        r = size if i % 2 == 0 else size * 0.4
        points.extend([cx + r * math.cos(angle), cy + r * math.sin(angle)])
    drawPolygon(*points, fill=color)

# ============================================================================
# PREMIUM ICON DRAWING - Beautiful, detailed icons for each category
# ============================================================================

def drawEventIcon(iconType, cx, cy, size):
    """Draw a beautiful, detailed icon for the event category"""
    # Outer glow effect
    drawCircle(cx, cy, size * 0.52, fill=rgb(240, 240, 245))
    # White circle background with shadow
    drawCircle(cx + 2, cy + 2, size * 0.48, fill=rgb(200, 200, 200))
    drawCircle(cx, cy, size * 0.48, fill='white')

    if iconType == 'tree':
        # TREE ICON - Detailed tree with layers
        # Tree trunk
        drawRect(cx - 4, cy + 8, 8, 18, fill=rgb(139, 90, 43))
        drawRect(cx - 3, cy + 8, 2, 18, fill=rgb(160, 110, 60))
        # Tree layers (3 triangular layers)
        # Bottom layer
        drawPolygon(cx - 18, cy + 10, cx + 18, cy + 10, cx, cy - 8, fill=rgb(34, 139, 34))
        # Middle layer
        drawPolygon(cx - 14, cy + 2, cx + 14, cy + 2, cx, cy - 16, fill=rgb(50, 160, 50))
        # Top layer
        drawPolygon(cx - 10, cy - 6, cx + 10, cy - 6, cx, cy - 22, fill=rgb(60, 179, 60))
        # Snow/highlight dots
        drawCircle(cx - 6, cy - 2, 2, fill='white')
        drawCircle(cx + 4, cy - 10, 2, fill='white')
        drawCircle(cx - 2, cy - 18, 1.5, fill='white')

    elif iconType == 'book':
        # BOOK ICON - Open book with pages
        # Book base (slightly angled)
        drawRect(cx - 20, cy - 12, 40, 28, fill=rgb(30, 100, 180))
        # Book spine
        drawRect(cx - 2, cy - 14, 4, 32, fill=rgb(20, 70, 140))
        # Left page
        drawRect(cx - 18, cy - 10, 15, 22, fill='white')
        # Right page
        drawRect(cx + 3, cy - 10, 15, 22, fill=rgb(248, 248, 248))
        # Page lines (left)
        for i in range(4):
            drawLine(cx - 16, cy - 5 + i * 5, cx - 5, cy - 5 + i * 5, fill=rgb(200, 200, 200), lineWidth=1)
        # Page lines (right)
        for i in range(4):
            drawLine(cx + 5, cy - 5 + i * 5, cx + 16, cy - 5 + i * 5, fill=rgb(200, 200, 200), lineWidth=1)
        # Bookmark ribbon
        drawPolygon(cx + 12, cy - 12, cx + 16, cy - 12, cx + 14, cy - 4, fill=rgb(220, 50, 50))

    elif iconType == 'box':
        # BOX ICON - Donation box with heart
        # Box shadow
        drawRect(cx - 16, cy - 6, 32, 26, fill=rgb(180, 120, 60))
        # Box body
        drawRect(cx - 18, cy - 8, 32, 26, fill=rgb(230, 160, 80))
        # Box front highlight
        drawRect(cx - 18, cy - 8, 32, 8, fill=rgb(245, 180, 100))
        # Box flaps (open)
        drawPolygon(cx - 18, cy - 8, cx - 22, cy - 16, cx - 6, cy - 16, cx - 2, cy - 8, fill=rgb(210, 140, 60))
        drawPolygon(cx + 2, cy - 8, cx + 6, cy - 16, cx + 22, cy - 16, cx + 18, cy - 8, fill=rgb(200, 130, 50))
        # Heart on box - cleaner
        hs = 6
        heartColor = rgb(220, 60, 80)
        drawCircle(cx - hs * 0.4, cy + 5, hs * 0.48, fill=heartColor)
        drawCircle(cx + hs * 0.4, cy + 5, hs * 0.48, fill=heartColor)
        drawPolygon(cx - hs * 0.75, cy + 6.5, cx + hs * 0.75, cy + 6.5, cx, cy + 12, fill=heartColor)

    elif iconType == 'heart':
        # HEART ICON - Clean, simple heart
        # Using a proper heart shape with bezier-like curves simulated
        heartColor = rgb(235, 80, 100)
        # Draw heart using overlapping shapes for smooth look
        s = 18  # scale
        # Left bump
        drawCircle(cx - s * 0.5, cy - s * 0.2, s * 0.55, fill=heartColor)
        # Right bump
        drawCircle(cx + s * 0.5, cy - s * 0.2, s * 0.55, fill=heartColor)
        # Bottom triangle
        drawPolygon(cx - s * 0.95, cy + s * 0.1,
                    cx + s * 0.95, cy + s * 0.1,
                    cx, cy + s * 1.1, fill=heartColor)
        # Small highlight
        drawCircle(cx - s * 0.35, cy - s * 0.35, s * 0.2, fill=rgb(255, 140, 160))

    elif iconType == 'palette':
        # PALETTE ICON - Artist palette with brush
        # Palette shape (oval)
        drawOval(cx, cy + 2, 36, 28, fill=rgb(222, 184, 135))
        drawOval(cx, cy, 34, 26, fill=rgb(245, 222, 179))
        # Thumb hole
        drawOval(cx - 10, cy + 6, 8, 6, fill='white')
        # Paint blobs
        drawCircle(cx - 8, cy - 6, 5, fill=rgb(220, 50, 50))  # Red
        drawCircle(cx + 2, cy - 8, 5, fill=rgb(50, 150, 220))  # Blue
        drawCircle(cx + 12, cy - 4, 4, fill=rgb(255, 220, 50))  # Yellow
        drawCircle(cx + 8, cy + 4, 4, fill=rgb(80, 200, 80))  # Green
        drawCircle(cx - 2, cy + 2, 3, fill=rgb(160, 80, 200))  # Purple
        # Paintbrush
        drawLine(cx + 16, cy - 12, cx + 26, cy - 22, fill=rgb(139, 90, 43), lineWidth=3)

    else:
        # DEFAULT STAR - Golden star
        drawStar(cx, cy, size * 0.35, 'gold')
        drawStar(cx, cy, size * 0.25, rgb(255, 230, 100))

def drawUserAvatar(cx, cy, size, name=''):
    """Draw a premium user avatar with gradient-like effect"""
    # Outer ring
    drawCircle(cx, cy, size + 2, fill=rgb(100, 100, 180))
    # Avatar background with gradient simulation
    drawCircle(cx, cy, size, fill=rgb(120, 100, 200))
    drawCircle(cx - size * 0.2, cy - size * 0.2, size * 0.6, fill=rgb(140, 120, 220))
    if name:
        parts = name.split()
        initials = ''.join(p[0].upper() for p in parts[:2]) if parts else '?'
    else:
        initials = '?'
    # Text shadow
    drawLabel(initials, cx + 1, cy + 1, size=size * 0.85, bold=True, fill=rgb(80, 60, 140), font='monospace')
    drawLabel(initials, cx, cy, size=size * 0.85, bold=True, fill='white', font='monospace')

def drawTinderHeart(cx, cy, size):
    """Draw a clean green heart for the like button"""
    s = size * 0.35  # scale
    heartColor = rgb(50, 200, 100)
    # Left bump
    drawCircle(cx - s * 0.45, cy - s * 0.15, s * 0.5, fill=heartColor)
    # Right bump
    drawCircle(cx + s * 0.45, cy - s * 0.15, s * 0.5, fill=heartColor)
    # Bottom point
    drawPolygon(cx - s * 0.85, cy + s * 0.15,
                cx + s * 0.85, cy + s * 0.15,
                cx, cy + s * 0.95,
                fill=heartColor)

def drawTinderX(cx, cy, size):
    """Draw a beautiful red X for the skip button"""
    t = size * 0.14
    # Shadow
    drawLine(cx - size * 0.22 + 1, cy - size * 0.22 + 1,
             cx + size * 0.22 + 1, cy + size * 0.22 + 1,
             fill=rgb(139, 0, 0), lineWidth=t)
    drawLine(cx + size * 0.22 + 1, cy - size * 0.22 + 1,
             cx - size * 0.22 + 1, cy + size * 0.22 + 1,
             fill=rgb(139, 0, 0), lineWidth=t)
    # Main X
    drawLine(cx - size * 0.22, cy - size * 0.22,
             cx + size * 0.22, cy + size * 0.22,
             fill=rgb(255, 99, 71), lineWidth=t)
    drawLine(cx + size * 0.22, cy - size * 0.22,
             cx - size * 0.22, cy + size * 0.22,
             fill=rgb(255, 99, 71), lineWidth=t)

def drawPremiumButton(x, y, w, h, text, color1, color2, textColor='white'):
    """Draw a premium button with gradient-like effect and shadow"""
    # Shadow
    drawRect(x + 3, y + 3, w, h, fill=rgb(180, 180, 180))
    # Button base
    drawRect(x, y, w, h, fill=color1)
    # Gradient simulation (lighter top half)
    drawRect(x, y, w, h * 0.5, fill=color2)
    # Text
    drawLabel(text, x + w/2, y + h/2, size=16, bold=True, fill=textColor, font='monospace')

def drawGlassCard(x, y, w, h):
    """Draw a card effect"""
    # Shadow
    drawRect(x + 4, y + 4, w, h, fill=rgb(220, 220, 220))
    # Main card
    drawRect(x, y, w, h, fill='white')
    # Border
    drawRect(x, y, w, h, fill=None, border=rgb(230, 230, 235), borderWidth=1)

# ============================================================================
# EVENT HANDLERS
# ============================================================================

def onMousePress(app, mouseX, mouseY):
    if app.mode == 'intro':
        # Button positions (matches drawIntroScreen)
        headerH = app.height * 0.55
        btnY1 = headerH + 55
        btnY2 = headerH + 125
        btnH = 50
        if btnY1 <= mouseY <= btnY1 + btnH:
            app.mode = 'signup'
        elif btnY2 <= mouseY <= btnY2 + btnH:
            app.mode = 'login'

    elif app.mode == 'login':
        cx = getCenterX(app)
        left = getLeftMargin(app)
        contentW = getContentWidth(app)
        fieldW = min(300, contentW - 20)
        fieldLeft = cx - fieldW/2
        toggleW = min(145, (contentW - 30) / 2)

        if mouseY <= 100 and mouseX <= left + 100:
            app.mode = 'intro'
        # Login type toggle
        elif 145 <= mouseY <= 185:
            if cx - toggleW - 5 <= mouseX <= cx - 5:
                app.loginType = 'volunteer'
            elif cx + 5 <= mouseX <= cx + toggleW + 5:
                app.loginType = 'organizer'
        elif 225 <= mouseY <= 270 and fieldLeft <= mouseX <= fieldLeft + fieldW:
            app.activeField = 'username'
        elif 305 <= mouseY <= 350 and fieldLeft <= mouseX <= fieldLeft + fieldW:
            app.activeField = 'password'
        elif 400 <= mouseY <= 450 and fieldLeft <= mouseX <= fieldLeft + fieldW:
            attemptLogin(app)
        elif 460 <= mouseY <= 500 and app.loginType == 'volunteer':
            app.mode = 'signup'
        else:
            app.activeField = None

    elif app.mode == 'orgDashboard':
        handleOrgDashboardClick(app, mouseX, mouseY)

    elif app.mode == 'orgEventDetail':
        if mouseY <= 60 and mouseX <= 100:
            app.mode = 'orgDashboard'
            app.selectedOrgEvent = None

    elif app.mode == 'createEvent':
        handleCreateEventClick(app, mouseX, mouseY)

    elif app.mode == 'signup':
        if mouseY <= 100 and mouseX <= 100:
            app.mode = 'intro'
        # Signup type toggle (y=138, height=35)
        elif 138 <= mouseY <= 173:
            if 50 <= mouseX <= 195:
                app.signupType = 'volunteer'
            elif 205 <= mouseX <= 350:
                app.signupType = 'organizer'
        else:
            # Calculate yOffset based on signup type
            yOffset = 65 if app.signupType == 'organizer' else 0

            # Name field (y=205, height=38)
            if 50 <= mouseX <= 350 and 205 <= mouseY <= 243:
                app.activeField = 'name'
            # Organization name field (only for organizers, y=270, height=38)
            elif app.signupType == 'organizer' and 50 <= mouseX <= 350 and 270 <= mouseY <= 308:
                app.activeField = 'orgname'
            # Username field (y=270+yOffset, height=38)
            elif 50 <= mouseX <= 350 and (270 + yOffset) <= mouseY <= (308 + yOffset):
                app.activeField = 'username'
            # Password field (y=335+yOffset, height=38)
            elif 50 <= mouseX <= 350 and (335 + yOffset) <= mouseY <= (373 + yOffset):
                app.activeField = 'password'
            # Signup button (y=420+yOffset, height=50)
            elif 50 <= mouseX <= 350 and (420 + yOffset) <= mouseY <= (470 + yOffset):
                attemptSignup(app)
            # Login link (around y=500+yOffset)
            elif (490 + yOffset) <= mouseY <= (520 + yOffset):
                app.mode = 'login'
            else:
                app.activeField = None

    elif app.mode == 'preferences':
        handlePreferencesClick(app, mouseX, mouseY)

    elif app.mode == 'swipe':
        handleSwipeClick(app, mouseX, mouseY)

    elif app.mode == 'allEvents':
        handleAllEventsClick(app, mouseX, mouseY)

    elif app.mode == 'saved':
        handleSavedClick(app, mouseX, mouseY)


    elif app.mode == 'eventDetail':
        if mouseY <= 60 and mouseX <= 100:
            app.mode = app.detailSource or 'swipe'
            app.selectedEvent = None
        elif 560 <= mouseY <= 610:
            if app.selectedEvent and app.selectedEvent not in app.savedEvents:
                app.savedEvents.append(app.selectedEvent)

    elif app.mode == 'verification':
        if abs(mouseX - 340) <= 15 and abs(mouseY - 220) <= 15:
            app.mode = 'saved'
            app.verificationEvent = None
        elif 440 <= mouseY <= 480 and len(app.verificationCode) == 4:
            attemptVerification(app)

    # Logout button on rewards screen
    elif app.mode == 'rewards':
        if 20 <= mouseY <= 50 and app.width - 70 <= mouseX <= app.width - 15:
            app.isLoggedIn = False
            app.currentUser = None
            app.userType = None
            app.mode = 'intro'
            return

    # Nav bar
    if app.mode in ['swipe', 'allEvents', 'saved', 'rewards']:
        if mouseY >= app.height - 60:
            tabWidth = app.width / 4
            tabIndex = int(mouseX // tabWidth)
            modes = ['swipe', 'allEvents', 'saved', 'rewards']
            if 0 <= tabIndex < 4:
                app.mode = modes[tabIndex]

def handlePreferencesClick(app, mouseX, mouseY):
    # Categories
    for i, cat in enumerate(app.categories):
        row = i // 2
        col = i % 2
        x = 30 + col * 175
        y = 140 + row * 50
        if x <= mouseX <= x + 160 and y <= mouseY <= y + 40:
            if cat in app.selectedCategories:
                app.selectedCategories.remove(cat)
            else:
                app.selectedCategories.add(cat)
            return

    # Time preference
    times = ['weekdays', 'weekends', 'either']
    for i, val in enumerate(times):
        x = 30 + i * 120
        if x <= mouseX <= x + 110 and 340 <= mouseY <= 380:
            app.timePreference = val
            return

    # Experience
    exps = ['new', 'experienced']
    for i, val in enumerate(exps):
        x = 30 + i * 175
        if x <= mouseX <= x + 160 and 440 <= mouseY <= 480:
            app.experienceLevel = val
            return

    # Continue
    if 520 <= mouseY <= 570 and len(app.selectedCategories) > 0 and app.timePreference:
        app.mode = 'swipe'
    elif 580 <= mouseY <= 620:
        app.mode = 'swipe'

def handleSwipeClick(app, mouseX, mouseY):
    cx = getCenterX(app)
    left = getLeftMargin(app)
    contentW = getContentWidth(app)

    # User avatar / logout (top right)
    avatarX = app.width - left - 25
    if abs(mouseX - avatarX) <= 20 and abs(mouseY - 30) <= 20:
        app.isLoggedIn = False
        app.currentUser = None
        app.userType = None
        app.mode = 'intro'
        return

    # Button positions (same as in drawSwipeScreen)
    cardH = min(480, app.height - 160)
    btnY = min(app.height - 75, 70 + cardH + 20)
    skipBtnX = cx - 80
    saveBtnX = cx + 80

    if app.currentEventIndex >= len(app.events):
        # "Browse All" button
        btnW = min(200, contentW - 60)
        if (cx - btnW/2 <= mouseX <= cx + btnW/2 and
            app.height/2 + 50 <= mouseY <= app.height/2 + 95):
            app.mode = 'allEvents'
        return

    # Skip button (X) - swipe left
    if abs(mouseX - skipBtnX) <= 35 and abs(mouseY - btnY) <= 35:
        handleSwipeAction(app, liked=False)
    # Save button (heart) - swipe right
    elif abs(mouseX - saveBtnX) <= 35 and abs(mouseY - btnY) <= 35:
        handleSwipeAction(app, liked=True)
    # Card area - for dragging
    elif 70 <= mouseY <= btnY - 30:
        app.isDragging = True
        app.dragStartX = mouseX

def handleAllEventsClick(app, mouseX, mouseY):
    # Logout button
    if 20 <= mouseY <= 50 and app.width - 70 <= mouseX <= app.width - 15:
        app.isLoggedIn = False
        app.currentUser = None
        app.userType = None
        app.mode = 'intro'
        return

    for i, event in enumerate(app.events[:5]):
        y = 80 + i * 90
        if y <= mouseY <= y + 80:
            if 312 <= mouseX <= 348:
                if event in app.savedEvents:
                    app.savedEvents.remove(event)
                else:
                    app.savedEvents.append(event)
            else:
                app.selectedEvent = event
                app.detailSource = 'allEvents'
                app.mode = 'eventDetail'
            return

def handleSavedClick(app, mouseX, mouseY):
    # Logout button
    if 20 <= mouseY <= 50 and app.width - 70 <= mouseX <= app.width - 15:
        app.isLoggedIn = False
        app.currentUser = None
        app.userType = None
        app.mode = 'intro'
        return

    for i, event in enumerate(app.savedEvents[:4]):
        y = 80 + i * 110
        if y <= mouseY <= y + 100:
            if 260 <= mouseX <= 350 and y + 65 <= mouseY <= y + 93:
                if event in app.completedEvents and event not in app.verifiedEvents:
                    app.verificationEvent = event
                    app.verificationCode = ''
                    app.verificationError = ''
                    app.mode = 'verification'
                elif event not in app.completedEvents:
                    app.completedEvents.append(event)
            else:
                app.selectedEvent = event
                app.detailSource = 'saved'
                app.mode = 'eventDetail'
            return

def handleOrgDashboardClick(app, mouseX, mouseY):
    # Logout button
    if 30 <= mouseY <= 60 and app.width - 80 <= mouseX <= app.width - 20:
        app.isLoggedIn = False
        app.currentUser = None
        app.userType = None
        app.mode = 'intro'
        return

    # Create Event button
    if 200 <= mouseY <= 245 and 20 <= mouseX <= 380:
        resetCreateEventForm(app)
        app.mode = 'createEvent'
        return

    # Event items
    orgEvents = getOrganizerEvents(app)
    for i, event in enumerate(orgEvents[:4]):
        y = 300 + i * 85
        if y <= mouseY <= y + 75:
            app.selectedOrgEvent = event
            app.mode = 'orgEventDetail'
            return

def resetCreateEventForm(app):
    app.newEventTitle = ''
    app.newEventDesc = ''
    app.newEventDate = ''
    app.newEventTime = ''
    app.newEventLocation = ''
    app.newEventHours = ''
    app.newEventCategory = None
    app.newEventImpact = 3
    app.createEventField = None
    app.createEventError = ''

def handleCreateEventClick(app, mouseX, mouseY):
    # Back button
    if mouseY <= 80 and mouseX <= 100:
        app.mode = 'orgDashboard'
        return

    # Title field
    if 118 <= mouseY <= 153 and 30 <= mouseX <= 370:
        app.createEventField = 'title'
    # Description field
    elif 178 <= mouseY <= 213 and 30 <= mouseX <= 370:
        app.createEventField = 'desc'
    # Date field
    elif 238 <= mouseY <= 273 and 30 <= mouseX <= 190:
        app.createEventField = 'date'
    # Time field
    elif 238 <= mouseY <= 273 and 210 <= mouseX <= 370:
        app.createEventField = 'time'
    # Location field
    elif 298 <= mouseY <= 333 and 30 <= mouseX <= 190:
        app.createEventField = 'location'
    # Hours field
    elif 298 <= mouseY <= 333 and 210 <= mouseX <= 370:
        app.createEventField = 'hours'
    # Category buttons
    elif 360 <= mouseY <= 430:
        for i, cat in enumerate(app.categories):
            x = 30 + (i % 3) * 115
            y = 360 + (i // 3) * 35
            if x <= mouseX <= x + 105 and y <= mouseY <= y + 28:
                app.newEventCategory = cat
                break
    # Impact stars
    elif 430 <= mouseY <= 455:
        for i in range(5):
            starX = 140 + i * 30
            if starX - 15 <= mouseX <= starX + 15:
                app.newEventImpact = i + 1
                break
    # Create button
    elif 500 <= mouseY <= 550 and 30 <= mouseX <= 370:
        createNewEvent(app)
    else:
        app.createEventField = None

def createNewEvent(app):
    # Validation
    if not app.newEventTitle:
        app.createEventError = 'Title is required'
        return
    if not app.newEventDesc:
        app.createEventError = 'Description is required'
        return
    if not app.newEventDate:
        app.createEventError = 'Date is required'
        return
    if not app.newEventTime:
        app.createEventError = 'Time is required'
        return
    if not app.newEventLocation:
        app.createEventError = 'Location is required'
        return
    if not app.newEventHours:
        app.createEventError = 'Hours is required'
        return
    if not app.newEventCategory:
        app.createEventError = 'Select a category'
        return

    try:
        hours = int(app.newEventHours)
    except:
        app.createEventError = 'Hours must be a number'
        return

    # Get organizer info
    orgName = app.organizers[app.currentUser]['org']

    # Generate unique ID and code
    newId = max(e['id'] for e in app.events) + 1
    code = app.newEventTitle[:4].upper().replace(' ', '')

    # Create new event
    newEvent = {
        'id': newId,
        'title': app.newEventTitle,
        'org': orgName,
        'category': app.newEventCategory,
        'desc': app.newEventDesc,
        'hours': hours,
        'date': app.newEventDate,
        'time': app.newEventTime,
        'location': app.newEventLocation,
        'mapX': 200,
        'mapY': 300,
        'impact': app.newEventImpact,
        'code': code
    }

    # Add to events list
    app.events.append(newEvent)
    saveEvents(app.events)

    # Reset form and go back
    resetCreateEventForm(app)
    app.mode = 'orgDashboard'

def onMouseDrag(app, mouseX, mouseY):
    if app.mode == 'swipe' and app.isDragging:
        app.cardOffsetX = mouseX - app.dragStartX

def onMouseRelease(app, mouseX, mouseY):
    if app.mode == 'swipe' and app.isDragging:
        app.isDragging = False

        if app.cardOffsetX > app.swipeThreshold:
            # Swiped right - liked
            handleSwipeAction(app, liked=True)
        elif app.cardOffsetX < -app.swipeThreshold:
            # Swiped left - skipped
            handleSwipeAction(app, liked=False)

        app.cardOffsetX = 0

def onKeyPress(app, key):
    if app.mode == 'login':
        handleLoginKey(app, key)
    elif app.mode == 'signup':
        handleSignupKey(app, key)
    elif app.mode == 'verification':
        handleVerificationKey(app, key)
    elif app.mode == 'createEvent':
        handleCreateEventKey(app, key)
    elif app.mode == 'swipe':
        if key == 'left':
            handleSwipeAction(app, liked=False)
        elif key == 'right' and app.currentEventIndex < len(app.events):
            handleSwipeAction(app, liked=True)

def handleCreateEventKey(app, key):
    field = app.createEventField
    if not field:
        return

    # Map field names to app attributes
    fieldMap = {
        'title': 'newEventTitle',
        'desc': 'newEventDesc',
        'date': 'newEventDate',
        'time': 'newEventTime',
        'location': 'newEventLocation',
        'hours': 'newEventHours'
    }

    if field not in fieldMap:
        return

    attr = fieldMap[field]
    currentValue = getattr(app, attr)

    if key == 'backspace':
        setattr(app, attr, currentValue[:-1])
    elif key == 'space':
        setattr(app, attr, currentValue + ' ')
    elif key == 'enter':
        createNewEvent(app)
    elif len(key) == 1:
        setattr(app, attr, currentValue + key)

    app.createEventError = ''

def handleLoginKey(app, key):
    if app.activeField == 'username':
        if key == 'backspace':
            app.loginUsername = app.loginUsername[:-1]
        elif key == 'tab':
            app.activeField = 'password'
        elif key == 'enter':
            attemptLogin(app)
        elif len(key) == 1:
            app.loginUsername += key
    elif app.activeField == 'password':
        if key == 'backspace':
            app.loginPassword = app.loginPassword[:-1]
        elif key == 'enter':
            attemptLogin(app)
        elif len(key) == 1:
            app.loginPassword += key

def handleSignupKey(app, key):
    if app.activeField == 'name':
        if key == 'backspace':
            app.signupName = app.signupName[:-1]
        elif key == 'tab':
            if app.signupType == 'organizer':
                app.activeField = 'orgname'
            else:
                app.activeField = 'username'
        elif key == 'space':
            app.signupName += ' '
        elif len(key) == 1:
            app.signupName += key
    elif app.activeField == 'orgname':
        if key == 'backspace':
            app.signupOrgName = app.signupOrgName[:-1]
        elif key == 'tab':
            app.activeField = 'username'
        elif key == 'space':
            app.signupOrgName += ' '
        elif len(key) == 1:
            app.signupOrgName += key
    elif app.activeField == 'username':
        if key == 'backspace':
            app.signupUsername = app.signupUsername[:-1]
        elif key == 'tab':
            app.activeField = 'password'
        elif len(key) == 1:
            app.signupUsername += key
    elif app.activeField == 'password':
        if key == 'backspace':
            app.signupPassword = app.signupPassword[:-1]
        elif key == 'enter':
            attemptSignup(app)
        elif len(key) == 1:
            app.signupPassword += key

def handleVerificationKey(app, key):
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

# ============================================================================
# AUTH & LOGIC
# ============================================================================

def attemptLogin(app):
    if not app.loginUsername or not app.loginPassword:
        app.loginError = 'Please fill in all fields'
        return

    # Check organizer login
    if app.loginType == 'organizer':
        if app.loginUsername in app.organizers:
            if app.organizers[app.loginUsername]['password'] == app.loginPassword:
                app.isLoggedIn = True
                app.currentUser = app.loginUsername
                app.userType = 'organizer'
                app.loginError = ''
                app.loginUsername = ''
                app.loginPassword = ''
                app.mode = 'orgDashboard'
                return
        app.loginError = 'Invalid organizer credentials'
        return

    # Check volunteer login
    if app.loginUsername in app.users:
        if app.users[app.loginUsername]['password'] == app.loginPassword:
            app.isLoggedIn = True
            app.currentUser = app.loginUsername
            app.userType = 'volunteer'
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

    # Check for organizer signup - needs org name
    if app.signupType == 'organizer' and not app.signupOrgName:
        app.signupError = 'Organization name required'
        return

    # Check username not taken in users or organizers
    if app.signupUsername in app.users or app.signupUsername in app.organizers:
        app.signupError = 'Username already taken'
        return

    if len(app.signupPassword) < 4:
        app.signupError = 'Password must be 4+ characters'
        return

    if app.signupType == 'organizer':
        # Create organizer account
        app.organizers[app.signupUsername] = {
            'password': app.signupPassword,
            'name': app.signupName,
            'org': app.signupOrgName
        }
        app.isLoggedIn = True
        app.currentUser = app.signupUsername
        app.userType = 'organizer'
        app.mode = 'orgDashboard'
    else:
        # Create volunteer account
        app.users[app.signupUsername] = {
            'password': app.signupPassword,
            'name': app.signupName
        }
        app.isLoggedIn = True
        app.currentUser = app.signupUsername
        app.userType = 'volunteer'
        app.mode = 'preferences'

        # Reset AI system for new volunteer user
        AI_givr.reset_ai_system()
        app.currentEventIndex = 0

    # Clear form
    app.signupName = ''
    app.signupUsername = ''
    app.signupPassword = ''
    app.signupOrgName = ''
    app.signupError = ''

def attemptVerification(app):
    if not app.verificationEvent:
        return

    if app.verificationCode.upper() == app.verificationEvent['code']:
        event = app.verificationEvent
        app.verifiedEvents.append(event)

        # Update rewards
        app.totalPoints += event['hours'] * 10 * event['impact']
        app.totalHours += event['hours']

        # Update tier
        for i in range(3, -1, -1):
            if app.totalPoints >= app.tierThresholds[i]:
                app.currentTier = i + 1
                break

        # First event badge
        if len(app.verifiedEvents) == 1:
            app.badges['first_event']['unlocked'] = True

        # 5 hours badge
        if app.totalHours >= 5:
            app.badges['five_hours']['unlocked'] = True

        app.weeklyStreak += 1
        app.mode = 'saved'
        app.verificationEvent = None
    else:
        app.verificationError = 'Incorrect code'

# ============================================================================
# AI EVENT GENERATION
# ============================================================================

def checkAndGenerateEvents(app):
    """
    Check how many events are left and, if low, ask the AI to generate more.
    Also persist the updated events list back to events.json.
    """
    remaining = len(app.events) - app.currentEventIndex

    if remaining <= app.minEventsBeforeGenerate:
        # Generate new personalized events
        newEvents = AI_givr.generate_new_events(app.events, count=3)

        if not newEvents:
            return

        # Make sure new events have unique IDs
        maxId = max((e.get('id', 0) for e in app.events), default=0)
        nextId = maxId + 1
        for ev in newEvents:
            if 'id' not in ev:
                ev['id'] = nextId
                nextId += 1

        # Add new events to the list
        app.events.extend(newEvents)

        # Save back to JSON so they persist (scraped + AI events live together)
        saveEvents(app.events)

def handleSwipeAction(app, liked):
    """
    Handle a swipe action (right=liked, left=skipped).
    Records preference and potentially generates new events.
    """
    if app.currentEventIndex >= len(app.events):
        return

    event = app.events[app.currentEventIndex]

    # Record the swipe with AI system
    if app.aiEnabled:
        AI_givr.record_swipe(event, liked)

    # Save event if liked
    if liked and event not in app.savedEvents:
        app.savedEvents.append(event)

    # Move to next event
    app.currentEventIndex += 1

    # Check if we need to generate more events
    if app.aiEnabled:
        checkAndGenerateEvents(app)

def main():
    runApp(width=400, height=700)

main()
