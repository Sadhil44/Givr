"""
Givr - Swipe to Give Back
Main UI using cmu_graphics
"""

from cmu_graphics import *
from givr_model import ALL_CATEGORIES, CATEGORY_COLORS, TIME_PREFERENCES
from givr_logic import (
    AppState, getTierName, getPointsForNextTier,
    ALL_BADGES, BADGE_DESCRIPTIONS
)

# ============ APP INITIALIZATION ============

def onAppStart(app):
    app.width = 400
    app.height = 700

    # Initialize app state
    app.state = AppState()
    app.state.loadAllEvents()

    # UI Constants
    app.bgColor = 'white'
    app.primaryColor = rgb(99, 102, 241)  # Indigo
    app.secondaryColor = rgb(139, 92, 246)  # Purple
    app.accentColor = rgb(236, 72, 153)  # Pink
    app.textColor = rgb(31, 41, 55)
    app.lightGray = rgb(243, 244, 246)
    app.medGray = rgb(156, 163, 175)

    # Tab bar
    app.tabs = ['Swipe', 'All', 'Saved', 'Map', 'Rewards']
    app.tabWidth = app.width / len(app.tabs)

    # Preference selection state (for multi-select)
    app.prefSelectedCats = set()
    app.prefSelectedTime = 'either'

# ============ DRAWING FUNCTIONS ============

def redrawAll(app):
    # Background
    drawRect(0, 0, app.width, app.height, fill='white')

    mode = app.state.mode

    if mode == 'intro':
        drawIntroScreen(app)
    elif mode == 'preferences':
        drawPreferencesScreen(app)
    elif mode == 'swipe':
        drawSwipeScreen(app)
        drawTabBar(app)
    elif mode == 'allEvents':
        drawAllEventsScreen(app)
        drawTabBar(app)
    elif mode == 'saved':
        drawSavedScreen(app)
        drawTabBar(app)
    elif mode == 'map':
        drawMapScreen(app)
        drawTabBar(app)
    elif mode == 'rewards':
        drawRewardsScreen(app)
        drawTabBar(app)
    elif mode == 'eventDetail':
        drawEventDetailScreen(app)

    # Verification dialog overlay
    if app.state.showVerifyDialog:
        drawVerifyDialog(app)

def drawIntroScreen(app):
    """Draw the intro/splash screen."""
    # Gradient-like background
    drawRect(0, 0, app.width, app.height, fill=app.primaryColor)
    drawRect(0, app.height//2, app.width, app.height//2,
             fill=gradient(app.primaryColor, app.secondaryColor, start='top'))

    # Logo area
    drawCircle(app.width//2, 200, 60, fill='white', opacity=20)
    drawCircle(app.width//2, 200, 45, fill='white', opacity=30)

    # App name
    drawLabel('Givr', app.width//2, 200, size=48, bold=True, fill='white')

    # Tagline
    drawLabel('Swipe to give back.', app.width//2, 270, size=18, fill='white', opacity=80)

    # Description
    drawLabel('Discover volunteer opportunities', app.width//2, 350, size=14, fill='white', opacity=70)
    drawLabel('that match your interests.', app.width//2, 370, size=14, fill='white', opacity=70)

    # Get Started button
    btnY = 480
    drawRect(app.width//2 - 100, btnY, 200, 50, fill='white', align='left-top')
    drawLabel('Get Started', app.width//2, btnY + 25, size=18, bold=True, fill=app.primaryColor)

def drawPreferencesScreen(app):
    """Draw the preferences selection screen."""
    # Header
    drawRect(0, 0, app.width, 80, fill=app.primaryColor)
    drawLabel('Set Your Preferences', app.width//2, 50, size=20, bold=True, fill='white')

    y = 110

    # Categories section
    drawLabel('What causes interest you?', app.width//2, y, size=16, bold=True, fill=app.textColor)
    y += 30

    # Category chips
    chipWidth = 170
    chipHeight = 40
    cols = 2
    padding = 15

    for i, cat in enumerate(ALL_CATEGORIES):
        col = i % cols
        row = i // cols
        x = 30 + col * (chipWidth + padding)
        chipY = y + row * (chipHeight + 10)

        isSelected = cat in app.prefSelectedCats
        bgFill = CATEGORY_COLORS.get(cat, 'gray') if isSelected else app.lightGray
        textFill = 'white' if isSelected else app.textColor

        drawRect(x, chipY, chipWidth, chipHeight, fill=bgFill, border=None)
        shortName = cat.split(' & ')[0][:15]
        drawLabel(shortName, x + chipWidth//2, chipY + chipHeight//2,
                  size=12, fill=textFill, bold=isSelected)

    y += (len(ALL_CATEGORIES) // cols + 1) * (chipHeight + 10) + 30

    # Time preference section
    drawLabel('When do you prefer to volunteer?', app.width//2, y, size=16, bold=True, fill=app.textColor)
    y += 35

    timeLabels = {'weekday': 'Weekdays', 'weekend': 'Weekends', 'either': 'Either'}
    btnWidth = 110
    startX = (app.width - 3 * btnWidth - 20) // 2

    for i, timeOpt in enumerate(TIME_PREFERENCES):
        bx = startX + i * (btnWidth + 10)
        isSelected = app.prefSelectedTime == timeOpt
        bgFill = app.primaryColor if isSelected else app.lightGray
        textFill = 'white' if isSelected else app.textColor

        drawRect(bx, y, btnWidth, 40, fill=bgFill)
        drawLabel(timeLabels[timeOpt], bx + btnWidth//2, y + 20,
                  size=13, fill=textFill, bold=isSelected)

    # Continue button
    btnY = 550
    drawRect(app.width//2 - 100, btnY, 200, 50, fill=app.primaryColor)
    drawLabel('Start Swiping', app.width//2, btnY + 25, size=16, bold=True, fill='white')

def drawSwipeScreen(app):
    """Draw the main swipe screen."""
    # Header
    drawRect(0, 0, app.width, 60, fill=app.primaryColor)
    drawLabel('Givr', app.width//2, 35, size=22, bold=True, fill='white')

    card = app.state.getCurrentCard()

    if card is None:
        # No more cards
        drawLabel("You're all caught up!", app.width//2, 300, size=20, bold=True, fill=app.textColor)
        drawLabel('Check back later for new events', app.width//2, 330, size=14, fill=app.medGray)

        # Options
        drawRect(app.width//2 - 80, 400, 160, 40, fill=app.lightGray)
        drawLabel('See All Events', app.width//2, 420, size=14, fill=app.textColor)
    else:
        # Draw the card with offset
        drawEventCard(app, card, app.width//2 + app.state.cardOffsetX, 330,
                      rotation=app.state.cardOffsetX * 0.02)

        # Swipe indicators
        if app.state.cardOffsetX > 30:
            drawLabel('SAVE', app.width//2 + 100, 150, size=24, bold=True,
                      fill='limeGreen', opacity=min(100, abs(app.state.cardOffsetX)))
        elif app.state.cardOffsetX < -30:
            drawLabel('SKIP', app.width//2 - 100, 150, size=24, bold=True,
                      fill='crimson', opacity=min(100, abs(app.state.cardOffsetX)))

        # Instructions
        drawLabel('Swipe right to save, left to skip', app.width//2, 580, size=12, fill=app.medGray)

def drawEventCard(app, event, cx, cy, rotation=0, width=320, height=420):
    """Draw a single event card."""
    x = cx - width//2
    y = cy - height//2

    # Card shadow
    drawRect(x + 4, y + 4, width, height, fill='gray', opacity=20)
    # Card background
    drawRect(x, y, width, height, fill='white', border=app.lightGray, borderWidth=1)

    # Category stripe at top
    catColor = CATEGORY_COLORS.get(event.category, 'gray')
    drawRect(x, y, width, 8, fill=catColor)

    # Content area
    contentY = y + 25

    # Category chip
    drawRect(x + 15, contentY, 120, 24, fill=catColor, opacity=80)
    drawLabel(event.category.split(' & ')[0], x + 75, contentY + 12, size=10, fill='white', bold=True)

    # Title
    contentY += 40
    drawLabel(event.title, x + width//2, contentY, size=18, bold=True, fill=app.textColor)

    # Organization
    contentY += 25
    drawLabel(event.organization, x + width//2, contentY, size=13, fill=app.medGray)

    # Divider
    contentY += 20
    drawLine(x + 20, contentY, x + width - 20, contentY, fill=app.lightGray)

    # Details row
    contentY += 25
    drawLabel(f'{event.hours} hours', x + 60, contentY, size=12, fill=app.textColor)
    drawLabel('|', x + 120, contentY, size=12, fill=app.lightGray)
    drawLabel(event.timeRange, x + 200, contentY, size=12, fill=app.textColor)

    contentY += 25
    drawLabel(event.date, x + width//2, contentY, size=12, fill=app.medGray)

    # Location
    contentY += 30
    drawCircle(x + 35, contentY, 8, fill=app.accentColor)
    drawLabel(event.locationName, x + 100, contentY, size=13, fill=app.textColor)

    # Description
    contentY += 35
    desc = event.description
    if len(desc) > 80:
        desc = desc[:77] + '...'
    # Word wrap (simple)
    words = desc.split()
    lines = []
    line = ''
    for w in words:
        if len(line + ' ' + w) < 35:
            line = line + ' ' + w if line else w
        else:
            lines.append(line)
            line = w
    if line:
        lines.append(line)

    for i, l in enumerate(lines[:3]):
        drawLabel(l, x + width//2, contentY + i * 18, size=12, fill=app.textColor)

def drawAllEventsScreen(app):
    """Draw the all events list screen."""
    # Header
    drawRect(0, 0, app.width, 60, fill=app.primaryColor)
    drawLabel('All Events', app.width//2, 35, size=20, bold=True, fill='white')

    # Filter chips
    y = 75
    chipWidth = 70
    startX = 15
    for i, cat in enumerate(['All'] + [c.split(' & ')[0][:8] for c in ALL_CATEGORIES]):
        isSelected = (i == 0 and app.state.allEventsFilterCategory is None) or \
                     (i > 0 and ALL_CATEGORIES[i-1] == app.state.allEventsFilterCategory)
        bgFill = app.primaryColor if isSelected else app.lightGray
        textFill = 'white' if isSelected else app.textColor

        if i < 3:
            drawRect(startX + i * (chipWidth + 5), y, chipWidth, 28, fill=bgFill)
            drawLabel(cat, startX + i * (chipWidth + 5) + chipWidth//2, y + 14, size=10, fill=textFill)
        elif i < 6:
            drawRect(startX + (i-3) * (chipWidth + 5), y + 33, chipWidth, 28, fill=bgFill)
            drawLabel(cat, startX + (i-3) * (chipWidth + 5) + chipWidth//2, y + 33 + 14, size=10, fill=textFill)

    # Event list
    events = app.state.allEvents
    if app.state.allEventsFilterCategory:
        events = [e for e in events if e.category == app.state.allEventsFilterCategory]

    listY = 150
    for i, event in enumerate(events[:6]):
        drawSmallEventCard(app, event, 20, listY + i * 75, app.width - 40, 70)

def drawSmallEventCard(app, event, x, y, w, h):
    """Draw a small event card for lists."""
    catColor = CATEGORY_COLORS.get(event.category, 'gray')

    drawRect(x, y, w, h, fill='white', border=app.lightGray, borderWidth=1)
    drawRect(x, y, 5, h, fill=catColor)

    # Title and org
    drawLabel(event.title[:25], x + 100, y + 18, size=13, bold=True, fill=app.textColor, align='left')
    drawLabel(event.organization[:30], x + 100, y + 36, size=11, fill=app.medGray, align='left')

    # Hours badge
    drawRect(x + 15, y + 15, 60, 40, fill=app.lightGray)
    drawLabel(f'{event.hours}h', x + 45, y + 28, size=14, bold=True, fill=app.textColor)
    drawLabel(event.dayType[:3], x + 45, y + 44, size=10, fill=app.medGray)

    # Save indicator
    if event.saved:
        drawLabel('Saved', x + w - 35, y + h//2, size=10, fill='limeGreen', bold=True)

def drawSavedScreen(app):
    """Draw the saved events screen."""
    # Header
    drawRect(0, 0, app.width, 60, fill=app.primaryColor)
    drawLabel('Saved Events', app.width//2, 35, size=20, bold=True, fill='white')

    if not app.state.savedEvents:
        drawLabel('No saved events yet', app.width//2, 300, size=16, fill=app.medGray)
        drawLabel('Swipe right on events to save them', app.width//2, 325, size=13, fill=app.medGray)
        return

    y = 80
    for i, event in enumerate(app.state.savedEvents[:7]):
        drawSavedEventCard(app, event, 15, y + i * 80, app.width - 30, 75)

def drawSavedEventCard(app, event, x, y, w, h):
    """Draw a saved event card with status."""
    catColor = CATEGORY_COLORS.get(event.category, 'gray')

    drawRect(x, y, w, h, fill='white', border=app.lightGray, borderWidth=1)
    drawRect(x, y, 5, h, fill=catColor)

    # Title
    drawLabel(event.title[:22], x + 15, y + 18, size=13, bold=True, fill=app.textColor, align='left')
    drawLabel(f'{event.hours}h - {event.locationName}', x + 15, y + 36, size=11, fill=app.medGray, align='left')

    # Status badge
    statusText = event.getStatusText()
    if event.verified:
        statusColor = 'limeGreen'
    elif event.completed:
        statusColor = 'orange'
    else:
        statusColor = app.medGray

    drawLabel(statusText, x + 15, y + 55, size=10, fill=statusColor, align='left')

    # Action button
    if not event.verified:
        btnText = 'Verify' if event.completed else 'Complete'
        btnColor = app.primaryColor if event.completed else app.secondaryColor
        drawRect(x + w - 75, y + 25, 65, 28, fill=btnColor)
        drawLabel(btnText, x + w - 42, y + 39, size=11, fill='white', bold=True)

def drawMapScreen(app):
    """Draw the map view screen."""
    # Header
    drawRect(0, 0, app.width, 60, fill=app.primaryColor)
    drawLabel('Event Map', app.width//2, 35, size=20, bold=True, fill='white')

    # Toggle filter
    toggleY = 75
    drawRect(15, toggleY, 85, 30, fill=app.primaryColor if not app.state.mapShowSavedOnly else app.lightGray)
    drawLabel('All', 57, toggleY + 15, size=12, fill='white' if not app.state.mapShowSavedOnly else app.textColor)

    drawRect(105, toggleY, 85, 30, fill=app.primaryColor if app.state.mapShowSavedOnly else app.lightGray)
    drawLabel('Saved', 147, toggleY + 15, size=12, fill='white' if app.state.mapShowSavedOnly else app.textColor)

    # Map area (stylized Pittsburgh)
    mapY = 120
    mapH = 450
    drawRect(10, mapY, app.width - 20, mapH, fill=rgb(230, 240, 230), border=app.lightGray)

    # Draw "rivers" (simplified)
    drawLine(50, mapY + 200, 200, mapY + 180, fill=rgb(173, 216, 230), lineWidth=8)
    drawLine(200, mapY + 180, app.width - 50, mapY + 220, fill=rgb(173, 216, 230), lineWidth=8)
    drawLine(200, mapY + 180, 200, mapY + 50, fill=rgb(173, 216, 230), lineWidth=8)

    # Neighborhood labels
    neighborhoods = [
        ('Downtown', 180, 220), ('Oakland', 280, 200), ('Shadyside', 320, 180),
        ('Lawrenceville', 260, 120), ('Strip', 200, 180), ('North Side', 160, 160),
        ('South Side', 220, 260), ('East Liberty', 340, 150), ('Squirrel Hill', 340, 220)
    ]
    for name, nx, ny in neighborhoods:
        drawLabel(name, nx, mapY + ny - 80, size=9, fill=app.medGray, italic=True)

    # Draw event pins
    events = app.state.savedEvents if app.state.mapShowSavedOnly else app.state.allEvents
    for event in events:
        px = event.mapX
        py = mapY + event.mapY - 80
        catColor = CATEGORY_COLORS.get(event.category, 'gray')

        # Pin
        drawCircle(px, py, 12, fill=catColor, border='white', borderWidth=2)
        if event.saved:
            drawStar(px, py, 5, 5, fill='white')

def drawRewardsScreen(app):
    """Draw the rewards and progress screen."""
    # Header
    drawRect(0, 0, app.width, 60, fill=app.primaryColor)
    drawLabel('Your Progress', app.width//2, 35, size=20, bold=True, fill='white')

    y = 80

    # Summary cards
    cardW = 170
    drawRect(20, y, cardW, 80, fill=app.lightGray)
    drawLabel('Verified Hours', 20 + cardW//2, y + 25, size=12, fill=app.medGray)
    drawLabel(str(app.state.totalVerifiedHours), 20 + cardW//2, y + 55, size=28, bold=True, fill=app.textColor)

    drawRect(200, y, cardW, 80, fill=app.lightGray)
    drawLabel('Impact Points', 200 + cardW//2, y + 25, size=12, fill=app.medGray)
    drawLabel(str(app.state.totalPoints), 200 + cardW//2, y + 55, size=28, bold=True, fill=app.primaryColor)

    y += 100

    # Current tier
    tier = app.state.currentTier
    tierName = getTierName(tier)
    nextTierPoints = getPointsForNextTier(tier)

    drawRect(20, y, app.width - 40, 90, fill='white', border=app.lightGray)
    drawLabel(f'Tier {tier}', 50, y + 25, size=14, fill=app.medGray, align='left')
    drawLabel(tierName, 50, y + 50, size=18, bold=True, fill=app.textColor, align='left')

    # Progress bar
    if tier < 4:
        progress = app.state.totalPoints / nextTierPoints
        barW = app.width - 80
        drawRect(40, y + 70, barW, 8, fill=app.lightGray)
        drawRect(40, y + 70, barW * min(1, progress), 8, fill=app.primaryColor)
        drawLabel(f'{app.state.totalPoints}/{nextTierPoints}', app.width - 50, y + 74, size=10, fill=app.medGray)
    else:
        drawLabel('Max tier reached!', app.width//2, y + 70, size=12, fill=app.accentColor)

    y += 110

    # Streak
    drawRect(20, y, app.width - 40, 50, fill=app.secondaryColor)
    drawLabel(f'{app.state.weeklyStreak} Week Streak', app.width//2, y + 25,
              size=16, bold=True, fill='white')

    y += 70

    # Badges section
    drawLabel('Badges', 30, y, size=16, bold=True, fill=app.textColor, align='left')
    y += 30

    badgeSize = 55
    cols = 4
    for i, badge in enumerate(ALL_BADGES):
        col = i % cols
        row = i // cols
        bx = 30 + col * (badgeSize + 15)
        by = y + row * (badgeSize + 25)

        isUnlocked = badge in app.state.unlockedBadges
        bgColor = app.primaryColor if isUnlocked else app.lightGray
        textColor = 'white' if isUnlocked else app.medGray

        drawCircle(bx + badgeSize//2, by + badgeSize//2, badgeSize//2, fill=bgColor)
        # Badge initial
        drawLabel(badge[0], bx + badgeSize//2, by + badgeSize//2 - 5, size=20, bold=True, fill=textColor)
        drawLabel(badge.split()[0][:8], bx + badgeSize//2, by + badgeSize + 10, size=9, fill=app.textColor)

def drawEventDetailScreen(app):
    """Draw the event detail screen."""
    event = app.state.detailEvent
    if not event:
        return

    # Header with back button
    drawRect(0, 0, app.width, 60, fill=app.primaryColor)
    drawLabel('< Back', 40, 35, size=14, fill='white')
    drawLabel('Event Details', app.width//2, 35, size=18, bold=True, fill='white')

    catColor = CATEGORY_COLORS.get(event.category, 'gray')

    y = 80

    # Category
    drawRect(20, y, 140, 30, fill=catColor)
    drawLabel(event.category, 90, y + 15, size=12, fill='white', bold=True)

    y += 50

    # Title
    drawLabel(event.title, app.width//2, y, size=22, bold=True, fill=app.textColor)
    y += 30
    drawLabel(event.organization, app.width//2, y, size=14, fill=app.medGray)

    y += 40

    # Details
    drawLine(20, y, app.width - 20, y, fill=app.lightGray)
    y += 20

    drawLabel(f'Date: {event.date}', 30, y, size=14, fill=app.textColor, align='left')
    y += 25
    drawLabel(f'Time: {event.timeRange}', 30, y, size=14, fill=app.textColor, align='left')
    y += 25
    drawLabel(f'Duration: {event.hours} hours', 30, y, size=14, fill=app.textColor, align='left')
    y += 25
    drawLabel(f'Location: {event.locationName}', 30, y, size=14, fill=app.textColor, align='left')

    y += 40

    # Description
    drawLine(20, y, app.width - 20, y, fill=app.lightGray)
    y += 20

    desc = event.description
    words = desc.split()
    lines = []
    line = ''
    for w in words:
        if len(line + ' ' + w) < 45:
            line = line + ' ' + w if line else w
        else:
            lines.append(line)
            line = w
    if line:
        lines.append(line)

    for l in lines[:4]:
        drawLabel(l, 30, y, size=13, fill=app.textColor, align='left')
        y += 20

    # Action buttons
    y = 550
    if event.saved:
        drawRect(app.width//2 - 80, y, 160, 45, fill=app.lightGray)
        drawLabel('Already Saved', app.width//2, y + 22, size=14, fill=app.medGray)
    else:
        drawRect(app.width//2 - 80, y, 160, 45, fill=app.primaryColor)
        drawLabel('Save Event', app.width//2, y + 22, size=14, bold=True, fill='white')

def drawVerifyDialog(app):
    """Draw the verification code dialog overlay."""
    # Dim background
    drawRect(0, 0, app.width, app.height, fill='black', opacity=50)

    # Dialog box
    dw, dh = 320, 220
    dx = (app.width - dw) // 2
    dy = (app.height - dh) // 2

    drawRect(dx, dy, dw, dh, fill='white')
    drawLabel('Enter Verification Code', dx + dw//2, dy + 30, size=16, bold=True, fill=app.textColor)
    drawLabel('Get the code from the event organizer', dx + dw//2, dy + 55, size=12, fill=app.medGray)

    # Input field
    inputY = dy + 90
    drawRect(dx + 30, inputY, dw - 60, 45, fill=app.lightGray)
    code = app.state.verifyCodeInput or ''
    drawLabel(code.upper() if code else 'Type code here...', dx + dw//2, inputY + 22,
              size=18, fill=app.textColor if code else app.medGray)

    # Error message
    if app.state.verifyError:
        drawLabel(app.state.verifyError, dx + dw//2, inputY + 55, size=12, fill='crimson')

    # Buttons
    btnY = dy + 160
    drawRect(dx + 30, btnY, 120, 40, fill=app.lightGray)
    drawLabel('Cancel', dx + 90, btnY + 20, size=14, fill=app.textColor)

    drawRect(dx + 170, btnY, 120, 40, fill=app.primaryColor)
    drawLabel('Verify', dx + 230, btnY + 20, size=14, bold=True, fill='white')

def drawTabBar(app):
    """Draw the bottom navigation tab bar."""
    tabY = app.height - 60
    drawRect(0, tabY, app.width, 60, fill='white', border=app.lightGray, borderWidth=1)

    modeToTab = {
        'swipe': 'Swipe', 'allEvents': 'All', 'saved': 'Saved',
        'map': 'Map', 'rewards': 'Rewards'
    }
    currentTab = modeToTab.get(app.state.mode, 'Swipe')

    for i, tab in enumerate(app.tabs):
        tx = i * app.tabWidth + app.tabWidth // 2
        isActive = tab == currentTab
        color = app.primaryColor if isActive else app.medGray

        # Icon placeholder (circle)
        drawCircle(tx, tabY + 20, 10, fill=color if isActive else 'white', border=color, borderWidth=2)
        drawLabel(tab, tx, tabY + 42, size=11, fill=color, bold=isActive)


# ============ EVENT HANDLERS ============

def onMousePress(app, mouseX, mouseY):
    state = app.state

    # Handle verification dialog first
    if state.showVerifyDialog:
        handleVerifyDialogClick(app, mouseX, mouseY)
        return

    if state.mode == 'intro':
        # Check Get Started button
        if 100 <= mouseX <= 300 and 480 <= mouseY <= 530:
            state.mode = 'preferences'

    elif state.mode == 'preferences':
        handlePreferencesClick(app, mouseX, mouseY)

    elif state.mode == 'swipe':
        # Start drag on card
        card = state.getCurrentCard()
        if card and 40 <= mouseX <= 360 and 120 <= mouseY <= 540:
            state.isDragging = True
            state.dragStartX = mouseX
            state.dragStartY = mouseY
        # Check empty deck buttons
        if card is None:
            if 120 <= mouseX <= 280 and 400 <= mouseY <= 440:
                state.mode = 'allEvents'
        # Tab bar
        handleTabClick(app, mouseX, mouseY)

    elif state.mode == 'allEvents':
        handleAllEventsClick(app, mouseX, mouseY)
        handleTabClick(app, mouseX, mouseY)

    elif state.mode == 'saved':
        handleSavedClick(app, mouseX, mouseY)
        handleTabClick(app, mouseX, mouseY)

    elif state.mode == 'map':
        handleMapClick(app, mouseX, mouseY)
        handleTabClick(app, mouseX, mouseY)

    elif state.mode == 'rewards':
        handleTabClick(app, mouseX, mouseY)

    elif state.mode == 'eventDetail':
        # Back button
        if mouseX <= 80 and mouseY <= 60:
            state.mode = 'allEvents'
        # Save button
        event = state.detailEvent
        if event and not event.saved:
            if 120 <= mouseX <= 280 and 550 <= mouseY <= 595:
                state.saveEvent(event)

def onMouseDrag(app, mouseX, mouseY):
    state = app.state

    if state.mode == 'swipe' and state.isDragging:
        state.cardOffsetX = mouseX - state.dragStartX
        state.cardOffsetY = (mouseY - state.dragStartY) * 0.3

def onMouseRelease(app, mouseX, mouseY):
    state = app.state

    if state.mode == 'swipe' and state.isDragging:
        # Check swipe threshold
        if state.cardOffsetX > 80:
            state.swipeRight()
        elif state.cardOffsetX < -80:
            state.swipeLeft()
        else:
            state.resetCardPosition()

def onKeyPress(app, key):
    state = app.state

    # Handle verification dialog input
    if state.showVerifyDialog:
        if key == 'backspace':
            state.verifyCodeInput = state.verifyCodeInput[:-1]
        elif key == 'escape':
            state.showVerifyDialog = False
            state.verifyCodeInput = ''
            state.verifyError = ''
        elif key == 'enter':
            attemptVerify(app)
        elif len(key) == 1 and key.isalnum() and len(state.verifyCodeInput) < 6:
            state.verifyCodeInput += key
        return

    # Quick navigation shortcuts
    if key == '1':
        state.mode = 'swipe'
    elif key == '2':
        state.mode = 'allEvents'
    elif key == '3':
        state.mode = 'saved'
    elif key == '4':
        state.mode = 'map'
    elif key == '5':
        state.mode = 'rewards'

    # Swipe shortcuts
    if state.mode == 'swipe':
        if key == 'right':
            state.swipeRight()
        elif key == 'left':
            state.swipeLeft()

def handlePreferencesClick(app, mouseX, mouseY):
    """Handle clicks on preferences screen."""
    # Category chips
    chipWidth = 170
    chipHeight = 40
    padding = 15
    y = 140

    for i, cat in enumerate(ALL_CATEGORIES):
        col = i % 2
        row = i // 2
        x = 30 + col * (chipWidth + padding)
        chipY = y + row * (chipHeight + 10)

        if x <= mouseX <= x + chipWidth and chipY <= mouseY <= chipY + chipHeight:
            if cat in app.prefSelectedCats:
                app.prefSelectedCats.remove(cat)
            else:
                app.prefSelectedCats.add(cat)
            return

    # Time preference buttons
    timeY = 340
    btnWidth = 110
    startX = (app.width - 3 * btnWidth - 20) // 2

    for i, timeOpt in enumerate(TIME_PREFERENCES):
        bx = startX + i * (btnWidth + 10)
        if bx <= mouseX <= bx + btnWidth and timeY <= mouseY <= timeY + 40:
            app.prefSelectedTime = timeOpt
            return

    # Continue button
    if 100 <= mouseX <= 300 and 550 <= mouseY <= 600:
        app.state.selectedCategories = app.prefSelectedCats.copy()
        app.state.timePreference = app.prefSelectedTime
        app.state.buildSwipeDeck()
        app.state.mode = 'swipe'

def handleAllEventsClick(app, mouseX, mouseY):
    """Handle clicks on all events screen."""
    # Filter chips
    y = 75
    chipWidth = 70
    startX = 15

    cats = [None] + ALL_CATEGORIES
    for i in range(6):
        row = 0 if i < 3 else 1
        col = i if i < 3 else i - 3
        cx = startX + col * (chipWidth + 5)
        cy = y + row * 33

        if cx <= mouseX <= cx + chipWidth and cy <= mouseY <= cy + 28:
            app.state.allEventsFilterCategory = cats[i] if i > 0 else None
            return

    # Event cards
    events = app.state.allEvents
    if app.state.allEventsFilterCategory:
        events = [e for e in events if e.category == app.state.allEventsFilterCategory]

    listY = 150
    for i, event in enumerate(events[:6]):
        cardY = listY + i * 75
        if 20 <= mouseX <= app.width - 20 and cardY <= mouseY <= cardY + 70:
            app.state.detailEvent = event
            app.state.mode = 'eventDetail'
            return

def handleSavedClick(app, mouseX, mouseY):
    """Handle clicks on saved screen."""
    if not app.state.savedEvents:
        return

    y = 80
    for i, event in enumerate(app.state.savedEvents[:7]):
        cardY = y + i * 80
        if 15 <= mouseX <= app.width - 15 and cardY <= mouseY <= cardY + 75:
            # Check action button click
            if mouseX >= app.width - 90:
                if not event.verified:
                    if event.completed:
                        # Show verify dialog
                        app.state.showVerifyDialog = True
                        app.state.verifyingEvent = event
                        app.state.verifyCodeInput = ''
                        app.state.verifyError = ''
                    else:
                        # Mark as completed
                        app.state.markCompleted(event)
                return
            # Otherwise show detail
            app.state.detailEvent = event
            app.state.mode = 'eventDetail'
            return

def handleMapClick(app, mouseX, mouseY):
    """Handle clicks on map screen."""
    # Toggle buttons
    if 15 <= mouseX <= 100 and 75 <= mouseY <= 105:
        app.state.mapShowSavedOnly = False
    elif 105 <= mouseX <= 190 and 75 <= mouseY <= 105:
        app.state.mapShowSavedOnly = True

    # Event pins (simplified - show detail for nearby clicks)
    mapY = 120
    events = app.state.savedEvents if app.state.mapShowSavedOnly else app.state.allEvents
    for event in events:
        px = event.mapX
        py = mapY + event.mapY - 80
        if abs(mouseX - px) < 20 and abs(mouseY - py) < 20:
            app.state.detailEvent = event
            app.state.mode = 'eventDetail'
            return

def handleVerifyDialogClick(app, mouseX, mouseY):
    """Handle clicks in verification dialog."""
    dw, dh = 320, 220
    dx = (app.width - dw) // 2
    dy = (app.height - dh) // 2
    btnY = dy + 160

    # Cancel button
    if dx + 30 <= mouseX <= dx + 150 and btnY <= mouseY <= btnY + 40:
        app.state.showVerifyDialog = False
        app.state.verifyCodeInput = ''
        app.state.verifyError = ''
        return

    # Verify button
    if dx + 170 <= mouseX <= dx + 290 and btnY <= mouseY <= btnY + 40:
        attemptVerify(app)
        return

def attemptVerify(app):
    """Attempt to verify the current event."""
    event = app.state.verifyingEvent
    code = app.state.verifyCodeInput

    if app.state.verifyEvent(event, code):
        app.state.showVerifyDialog = False
        app.state.verifyCodeInput = ''
        app.state.verifyError = ''
        app.state.verifyingEvent = None
    else:
        app.state.verifyError = 'Incorrect code. Try again.'

def handleTabClick(app, mouseX, mouseY):
    """Handle clicks on the tab bar."""
    tabY = app.height - 60
    if mouseY < tabY:
        return

    tabIndex = int(mouseX // app.tabWidth)
    modes = ['swipe', 'allEvents', 'saved', 'map', 'rewards']
    if 0 <= tabIndex < len(modes):
        app.state.mode = modes[tabIndex]


# ============ RUN APP ============

def main():
    runApp(width=400, height=700)

if __name__ == '__main__':
    main()
