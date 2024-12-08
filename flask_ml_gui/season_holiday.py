from datetime import datetime

# Define the seasons
def get_season(date):
    year = date.year
    seasons = {
        "Winter": [(1, 1), (3, 19)],   # Jan 1 to Mar 19
        "Spring": [(3, 20), (6, 20)],  # Mar 20 to Jun 20
        "Summer": [(6, 21), (9, 21)],  # Jun 21 to Sep 21
        "Fall": [(9, 22), (12, 20)],   # Sep 22 to Dec 20
        "Winter": [(12, 21), (12, 31)] # Dec 21 to Dec 31
    }
    
    for season, (start, end) in seasons.items():
        start_date = datetime(year, *start)
        end_date = datetime(year, *end)
        if start_date <= date <= end_date:
            return season
    return "Unknown"

# Define holidays
HOLIDAYS = {
    "New Year's Day": (1, 1),
    "Independence Day": (7, 4),
    "Christmas Day": (12, 25),
    "Thanksgiving Day (2024)": (11, 28), # Adjust based on year
    # Add more holidays as needed
}

def is_holiday(date):
    for holiday, (month, day) in HOLIDAYS.items():
        if date.month == month and date.day == day:
            return holiday
    return None