from cmu_graphics import *
import math

# ============================================================================
# GIVR - Swipe to Give Back
# Simple UI using cmu_graphics
# ============================================================================

def onAppStart(app):
    app.width = 400
    app.height = 700

    # Navigation state
    app.mode = 'intro'

    # User state
    app.isLoggedIn = False
    app.currentUser = None
    app.userType = None  # 'volunteer' or 'organizer'
    app.users = {}

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
    app.events = createSampleEvents()
    app.currentEventIndex = 0
    app.savedEvents = []
    app.completedEvents = []
    app.verifiedEvents = []

    # Swipe state
    app.isDragging = False
    app.dragStartX = 0
    app.cardOffsetX = 0
    app.swipeThreshold = 80

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

def createSampleEvents():
    return [
        {
            'id': 1, 'title': 'Park Cleanup',
            'org': 'Pittsburgh Parks', 'category': 'Environment',
            'desc': 'Help clean up Schenley Park',
            'hours': 3, 'date': 'Sat, Nov 25', 'time': '10AM-1PM',
            'location': 'Oakland', 'mapX': 280, 'mapY': 320,
            'impact': 3, 'code': 'PARK'
        },
        {
            'id': 2, 'title': 'Youth Tutoring',
            'org': 'CMU Tutoring', 'category': 'Education',
            'desc': 'Tutor middle school students',
            'hours': 2, 'date': 'Mon, Nov 27', 'time': '4PM-6PM',
            'location': 'East Liberty', 'mapX': 320, 'mapY': 250,
            'impact': 4, 'code': 'TUTR'
        },
        {
            'id': 3, 'title': 'Food Bank',
            'org': 'PGH Food Bank', 'category': 'Community',
            'desc': 'Sort food donations',
            'hours': 4, 'date': 'Sun, Nov 26', 'time': '9AM-1PM',
            'location': 'Downtown', 'mapX': 150, 'mapY': 400,
            'impact': 5, 'code': 'FOOD'
        },
        {
            'id': 4, 'title': 'Senior Visit',
            'org': 'Senior Center', 'category': 'Health',
            'desc': 'Spend time with seniors',
            'hours': 2, 'date': 'Wed, Nov 29', 'time': '2PM-4PM',
            'location': 'Friendship', 'mapX': 300, 'mapY': 280,
            'impact': 4, 'code': 'SNRS'
        },
        {
            'id': 5, 'title': 'Art Workshop',
            'org': 'Arts Council', 'category': 'Arts',
            'desc': 'Help run painting workshop',
            'hours': 3, 'date': 'Sat, Dec 2', 'time': '1PM-4PM',
            'location': 'Shadyside', 'mapX': 340, 'mapY': 300,
            'impact': 3, 'code': 'ARTS'
        },
        {
            'id': 6, 'title': 'Trail Cleanup',
            'org': 'Heritage Trail', 'category': 'Environment',
            'desc': 'Maintain riverfront trails',
            'hours': 4, 'date': 'Sat, Dec 9', 'time': '8AM-12PM',
            'location': 'North Shore', 'mapX': 120, 'mapY': 280,
            'impact': 4, 'code': 'RIVR'
        },
        {
            'id': 7, 'title': 'Homework Help',
            'org': 'Boys & Girls Club', 'category': 'Education',
            'desc': 'Help kids with homework',
            'hours': 2, 'date': 'Tue, Nov 28', 'time': '3:30PM-5:30PM',
            'location': 'Hill District', 'mapX': 180, 'mapY': 350,
            'impact': 4, 'code': 'HMWK'
        },
        {
            'id': 8, 'title': 'Mural Project',
            'org': 'Sprout Fund', 'category': 'Arts',
            'desc': 'Paint community mural',
            'hours': 5, 'date': 'Sun, Dec 3', 'time': '10AM-3PM',
            'location': 'Lawrenceville', 'mapX': 250, 'mapY': 220,
            'impact': 4, 'code': 'MURL'
        },
    ]

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
    # Header
    drawRect(0, 0, app.width, 350, fill='mediumSlateBlue')

    # Logo circle
    drawCircle(app.width/2, 180, 60, fill='white')
    drawLabel('G', app.width/2, 180, size=50, bold=True, fill='mediumSlateBlue', font='monospace')

    # App name
    drawLabel('Givr', app.width/2, 280, size=40, bold=True, fill='white', font='monospace')
    drawLabel('Swipe to give back', app.width/2, 320, size=16, fill='white', font='monospace')

    # Buttons
    drawRect(50, 420, 300, 50, fill='mediumSlateBlue')
    drawLabel('Get Started', app.width/2, 445, size=18, bold=True, fill='white', font='monospace')

    drawRect(50, 490, 300, 50, fill='white', border='mediumSlateBlue', borderWidth=2)
    drawLabel('Log In', app.width/2, 515, size=18, bold=True, fill='mediumSlateBlue', font='monospace')

def drawLoginScreen(app):
    # Header
    drawRect(0, 0, app.width, 100, fill='mediumSlateBlue')
    drawLabel('< Back', 50, 50, size=16, fill='white', align='left', font='monospace')
    drawLabel('Log In', app.width/2, 50, size=24, bold=True, fill='white', font='monospace')

    # Login type toggle
    drawLabel('I am a:', app.width/2, 130, size=14, fill='black', font='monospace')

    volActive = app.loginType == 'volunteer'
    orgActive = app.loginType == 'organizer'

    drawRect(50, 145, 145, 40, fill='mediumSlateBlue' if volActive else 'lightGray')
    drawLabel('Volunteer', 122, 165, size=14, fill='white' if volActive else 'black', font='monospace')

    drawRect(205, 145, 145, 40, fill='darkSlateBlue' if orgActive else 'lightGray')
    drawLabel('Organizer', 277, 165, size=14, fill='white' if orgActive else 'black', font='monospace')

    # Form
    drawLabel('Username', 50, 210, size=14, fill='gray', align='left', font='monospace')
    border = 'mediumSlateBlue' if app.activeField == 'username' else 'lightGray'
    drawRect(50, 225, 300, 45, fill='white', border=border, borderWidth=2)
    text = app.loginUsername if app.loginUsername else 'Enter username'
    color = 'black' if app.loginUsername else 'lightGray'
    drawLabel(text, 65, 247, size=16, fill=color, align='left', font='monospace')

    drawLabel('Password', 50, 290, size=14, fill='gray', align='left', font='monospace')
    border = 'mediumSlateBlue' if app.activeField == 'password' else 'lightGray'
    drawRect(50, 305, 300, 45, fill='white', border=border, borderWidth=2)
    text = '*' * len(app.loginPassword) if app.loginPassword else 'Enter password'
    color = 'black' if app.loginPassword else 'lightGray'
    drawLabel(text, 65, 327, size=16, fill=color, align='left', font='monospace')

    if app.loginError:
        drawLabel(app.loginError, app.width/2, 370, size=14, fill='red', font='monospace')

    # Login button
    btnColor = 'darkSlateBlue' if app.loginType == 'organizer' else 'mediumSlateBlue'
    drawRect(50, 400, 300, 50, fill=btnColor)
    drawLabel('Log In', app.width/2, 425, size=18, bold=True, fill='white', font='monospace')

    # Sign up link (only for volunteers)
    if app.loginType == 'volunteer':
        drawLabel("Don't have an account? Sign Up", app.width/2, 480, size=14, fill='mediumSlateBlue', font='monospace')
    else:
        drawLabel('Organizer accounts are pre-registered', app.width/2, 480, size=12, fill='gray', font='monospace')

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
    # Header
    drawRect(0, 0, app.width, 60, fill='white', border='lightGray', borderWidth=1)
    drawLabel('Givr', 30, 35, size=24, bold=True, fill='mediumSlateBlue', align='left', font='monospace')

    # Logout button
    drawRect(app.width - 70, 20, 55, 30, fill='lightGray')
    drawLabel('Logout', app.width - 42, 35, size=10, fill='gray', font='monospace')

    if app.currentEventIndex >= len(app.events):
        # Empty state
        drawLabel('All caught up!', app.width/2, 300, size=24, bold=True, fill='gray', font='monospace')
        drawLabel('Check back for more events', app.width/2, 340, size=14, fill='lightGray', font='monospace')

        drawRect(80, 400, 240, 45, fill='mediumSlateBlue')
        drawLabel('See All Events', app.width/2, 422, size=16, fill='white', font='monospace')
    else:
        # Draw card
        event = app.events[app.currentEventIndex]
        drawEventCard(app, event, 30 + app.cardOffsetX, 80)

        # Swipe indicators
        if app.cardOffsetX > 20:
            drawLabel('SAVE', app.width/2, 120, size=28, bold=True, fill='green', font='monospace')
        elif app.cardOffsetX < -20:
            drawLabel('SKIP', app.width/2, 120, size=28, bold=True, fill='red', font='monospace')

        # Action buttons
        drawCircle(100, 560, 28, fill='white', border='red', borderWidth=3)
        drawLabel('X', 100, 560, size=20, bold=True, fill='red', font='monospace')

        drawCircle(300, 560, 28, fill='white', border='green', borderWidth=3)
        drawLabel('+', 300, 560, size=24, bold=True, fill='green', font='monospace')

        drawLabel(f'{app.currentEventIndex + 1} / {len(app.events)}', app.width/2, 560, size=14, fill='gray')

    drawNavBar(app, 0)

def drawEventCard(app, event, x, y):
    cardW = 340
    cardH = 420

    # Card shadow
    drawRect(x + 3, y + 3, cardW, cardH, fill='lightGray')
    # Card
    drawRect(x, y, cardW, cardH, fill='white', border='lightGray', borderWidth=1)

    # Category banner
    catColor = app.categoryColors.get(event['category'], 'gray')
    drawRect(x, y, cardW, 50, fill=catColor)
    drawLabel(event['category'], x + 15, y + 25, size=14, fill='white', align='left', bold=True, font='monospace')
    drawLabel(f"{event['hours']}h", x + cardW - 40, y + 25, size=14, fill='white', bold=True, font='monospace')

    # Title and org
    drawLabel(event['title'], x + cardW/2, y + 85, size=22, bold=True, fill='black', font='monospace')
    drawLabel(event['org'], x + cardW/2, y + 115, size=14, fill='gray', font='monospace')

    # Line
    drawLine(x + 20, y + 140, x + cardW - 20, y + 140, fill='lightGray')

    # Description
    drawLabel(event['desc'], x + cardW/2, y + 170, size=14, fill='black', font='monospace')

    # Details
    drawLabel('Date:', x + 30, y + 220, size=12, fill='gray', align='left', font='monospace')
    drawLabel(event['date'], x + 100, y + 220, size=12, fill='black', align='left', font='monospace')

    drawLabel('Time:', x + 30, y + 250, size=12, fill='gray', align='left', font='monospace')
    drawLabel(event['time'], x + 100, y + 250, size=12, fill='black', align='left', font='monospace')

    drawLabel('Location:', x + 30, y + 280, size=12, fill='gray', align='left', font='monospace')
    drawLabel(event['location'], x + 100, y + 280, size=12, fill='black', align='left', font='monospace')

    # Impact
    drawLabel('Impact:', x + 30, y + 330, size=12, fill='gray', align='left', font='monospace')
    for i in range(5):
        starColor = 'gold' if i < event['impact'] else 'lightGray'
        drawStar(x + 100 + i * 25, y + 330, 10, starColor)

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

    # Badges
    drawLabel('Badges', 30, 380, size=16, bold=True, fill='black', align='left', font='monospace')

    badgeList = list(app.badges.items())
    for i, (key, badge) in enumerate(badgeList):
        x = 50 + (i % 4) * 85
        y = 410 + (i // 4) * 80

        color = 'gold' if badge['unlocked'] else 'lightGray'
        drawCircle(x, y, 25, fill=color)
        drawLabel('?' if not badge['unlocked'] else 'B', x, y, size=16, fill='white', bold=True, font='monospace')
        drawLabel(badge['name'], x, y + 40, size=9, fill='gray', font='monospace')

    drawNavBar(app, 3)  # Rewards is now index 3

def drawEventDetailScreen(app):
    if not app.selectedEvent:
        return

    event = app.selectedEvent
    catColor = app.categoryColors.get(event['category'], 'gray')

    # Header
    drawRect(0, 0, app.width, 120, fill=catColor)
    drawLabel('< Back', 40, 40, size=16, fill='white', align='left', font='monospace')
    drawLabel(event['category'], app.width/2, 40, size=14, fill='white', bold=True, font='monospace')
    drawLabel(event['title'], app.width/2, 80, size=22, bold=True, fill='white', font='monospace')
    drawLabel(event['org'], app.width/2, 105, size=14, fill='white', font='monospace')

    # Details
    drawRect(20, 140, 360, 400, fill='white', border='lightGray', borderWidth=1)

    drawLabel('About', 40, 170, size=14, bold=True, fill='black', align='left', font='monospace')
    drawLabel(event['desc'], 40, 200, size=13, fill='black', align='left', font='monospace')

    drawLine(40, 230, 360, 230, fill='lightGray')

    details = [
        ('Date', event['date']),
        ('Time', event['time']),
        ('Location', event['location']),
        ('Hours', str(event['hours']))
    ]

    for i, (label, value) in enumerate(details):
        y = 260 + i * 35
        drawLabel(label, 40, y, size=12, fill='gray', align='left', font='monospace')
        drawLabel(value, 360, y, size=13, fill='black', align='right', font='monospace')

    # Impact
    drawLabel('Impact', 40, 410, size=12, fill='gray', align='left', font='monospace')
    for i in range(5):
        color = 'gold' if i < event['impact'] else 'lightGray'
        drawStar(280 + i * 22, 410, 8, color)

    # Save button
    isSaved = event in app.savedEvents
    btnText = 'Saved!' if isSaved else 'Save Event'
    btnColor = 'green' if isSaved else 'mediumSlateBlue'
    drawRect(50, 560, 300, 50, fill=btnColor)
    drawLabel(btnText, app.width/2, 585, size=18, bold=True, fill='white', font='monospace')

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
    y = app.height - 60
    drawRect(0, y, app.width, 60, fill='white', border='lightGray', borderWidth=1)

    tabs = ['Swipe', 'Events', 'Saved', 'Rewards']
    tabWidth = app.width / 4

    for i, tab in enumerate(tabs):
        x = i * tabWidth + tabWidth / 2
        color = 'mediumSlateBlue' if i == activeIndex else 'gray'
        drawLabel(tab, x, y + 35, size=11, fill=color, bold=(i == activeIndex), font='monospace')

def drawStar(cx, cy, size, color):
    points = []
    for i in range(10):
        angle = math.radians(i * 36 - 90)
        r = size if i % 2 == 0 else size * 0.4
        points.extend([cx + r * math.cos(angle), cy + r * math.sin(angle)])
    drawPolygon(*points, fill=color)

# ============================================================================
# EVENT HANDLERS
# ============================================================================

def onMousePress(app, mouseX, mouseY):
    if app.mode == 'intro':
        if 420 <= mouseY <= 470:
            app.mode = 'signup'
        elif 490 <= mouseY <= 540:
            app.mode = 'login'

    elif app.mode == 'login':
        if mouseY <= 100 and mouseX <= 100:
            app.mode = 'intro'
        # Login type toggle
        elif 145 <= mouseY <= 185:
            if 50 <= mouseX <= 195:
                app.loginType = 'volunteer'
            elif 205 <= mouseX <= 350:
                app.loginType = 'organizer'
        elif 225 <= mouseY <= 270:
            app.activeField = 'username'
        elif 305 <= mouseY <= 350:
            app.activeField = 'password'
        elif 400 <= mouseY <= 450:
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
    # Logout button
    if 20 <= mouseY <= 50 and app.width - 70 <= mouseX <= app.width - 15:
        app.isLoggedIn = False
        app.currentUser = None
        app.userType = None
        app.mode = 'intro'
        return

    if app.currentEventIndex >= len(app.events):
        if 400 <= mouseY <= 445:
            app.mode = 'allEvents'
        return

    # Skip button
    if 72 <= mouseX <= 128 and 532 <= mouseY <= 588:
        app.currentEventIndex += 1
    # Save button
    elif 272 <= mouseX <= 328 and 532 <= mouseY <= 588:
        event = app.events[app.currentEventIndex]
        if event not in app.savedEvents:
            app.savedEvents.append(event)
        app.currentEventIndex += 1
    # Card area
    elif 80 <= mouseY <= 500:
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
            if app.currentEventIndex < len(app.events):
                event = app.events[app.currentEventIndex]
                if event not in app.savedEvents:
                    app.savedEvents.append(event)
                app.currentEventIndex += 1
        elif app.cardOffsetX < -app.swipeThreshold:
            app.currentEventIndex += 1

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
            app.currentEventIndex += 1
        elif key == 'right' and app.currentEventIndex < len(app.events):
            event = app.events[app.currentEventIndex]
            if event not in app.savedEvents:
                app.savedEvents.append(event)
            app.currentEventIndex += 1

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

def main():
    runApp(width=400, height=700)

main()
