"""Deterministic housing search tools used in the webinar."""


LISTINGS = [
    {"name": "Cedar Park Townhome", "area": "Cedar Park", "rent": 2300, "beds": 3},
    {"name": "Mueller Condo", "area": "Mueller", "rent": 2450, "beds": 2},
    {"name": "Downtown Loft", "area": "Downtown", "rent": 2900, "beds": 1},
]

NEIGHBORHOODS = {
    "Cedar Park": {"commute": "35 minutes", "character": "suburban and quiet"},
    "Mueller": {"commute": "18 minutes", "character": "walkable and family-friendly"},
    "Downtown": {"commute": "8 minutes", "character": "urban and lively"},
}


def search_listings(max_rent):
    """Return listings at or below the requested monthly rent."""
    return [home for home in LISTINGS if home["rent"] <= max_rent]


def get_neighborhoods():
    """Return the neighborhood facts available to the agent."""
    return NEIGHBORHOODS
