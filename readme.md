# Givr - Swipe to Give Back

A Tinder-style volunteer discovery app for CMU students built with cmu_graphics.

## Award Categories
- Best UI/UX
- Most Impactful

## External Modules
- **cmu_graphics** (bundled in project) - No additional installation needed

## How to Run
```bash
python main.py
```

## Description
Givr makes finding volunteer opportunities as easy as swiping through a dating app. Users can:
- Set preferences for cause categories and time availability
- Swipe through curated volunteer events (right to save, left to skip)
- Browse all events in a list view with filtering
- View saved events and track completion status
- See events on a stylized map of Pittsburgh
- Earn points, badges, and tier progression through verified volunteering

## Controls

### Navigation
- Click tabs at the bottom to switch between screens
- Keyboard shortcuts: 1-5 for quick navigation

### Swiping
- Drag cards left/right with mouse to skip/save
- Arrow keys (left/right) also work for swiping

### Verification
- After attending an event, mark it "Complete" in Saved
- Enter the 4-letter verification code to confirm attendance
- Codes for testing: PARK, TUTR, FOOD, CARE, ARTS, etc.

## Project Structure
- `main.py` - Main UI using cmu_graphics (entry point)
- `givr_model.py` - Data structures and event loading
- `givr_logic.py` - App state, rewards, and game logic
- `data/events.json` - Sample volunteer event data
