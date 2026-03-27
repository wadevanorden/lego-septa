STOPS_TO_PINS = {
    "Malvern": 0,
    "Paoli": 1,
    "Bryn Mawr": 2,
    "30th": 3,
    "Suburban Station": 4,
    "Jefferson Station": 5,
    "North Broad": 6,
    "Cynwyd": 7,
    "Norristown": 8,
    "Chestnut Hill West": 9,
    "Chestnut Hill East": 10,
    "Doylestown": 11,
    "Lansdale": 12,
    "Warminster": 13,
    "Glenside": 14,
    "West Trenton": 15,
    "Fox Chase": 16,
    "North Philadelphia": 17,
    "Wawa": 18,
    "Newark DE": 19,
    "Wilmington": 20,
    "Airport": 21,
    "Marcus Hook": 22,
    "Thorndale": 23,
    "Wayne Junction": 24,
    "Trenton": 25
}

STOPS = [
    "Thorndale",
    "Malvern",
    "Paoli",
    "Bryn Mawr",
    "30th",
    "Suburban Station",
    "Jefferson Station",
    "North Broad",
    "Cynwyd",
    "Norristown",
    "Chestnut Hill West",
    "Chestnut Hill East",
    "Doylestown",
    "Lansdale",
    "Warminster",
    "Glenside",
    "West Trenton",
    "Fox Chase",
    "North Philadelphia Septa",
    "North Philadelphia Amtrak",
    "Wawa",
    "Newark DE",
    "Wilmington",
    "Marcus Hook",
    "Airport Terminal A",
    "Airport Terminal B",
    "Airport Terminal C D",
    "Airport Terminal E F",
    "Wayne Junction",
    "Trenton"
]

AIRPORT_STOPS = [
    "Airport Terminal A",
    "Airport Terminal B",
    "Airport Terminal C D",
    "Airport Terminal E F"
]

NORTH_PHILLY_STOPS = [
    "North Philadelphia Septa",
    "North Philadelphia Amtrak"
]

ROUTES = [
    "AIR",
    "CHE",
    "CHW",
    "CYN",
    "FOX",
    "GLN",
    "LAN",
    "MED",
    "NOR",
    "PAO",
    "TRE",
    "WAR",
    "WIL",
    "WTR"
]

STOPS_TO_ROUTES = {
    "Thorndale": ["PAO"],
    "Malvern": ["PAO"],
    "Paoli": ["PAO"],
    "Bryn Mawr": ["PAO"],
    "30th": ["PAO", "CHE", "CHW", "CYN", "FOX", "GLN", "LAN", "MED", "NOR", "TRE", "WAR", "WIL", "WTR", "AIR"],
    "Suburban Station": ["PAO", "CHE", "CHW", "CYN", "FOX", "GLN", "LAN", "MED", "NOR", "TRE", "WAR", "WIL", "WTR", "AIR"],
    "Jefferson Station": ["PAO", "CHE", "CHW", "FOX", "GLN", "LAN", "MED", "NOR", "TRE", "WAR", "WIL", "WTR", "AIR"],
    "North Broad": ["CHW", "GLN", "LAN", "NOR"],
    "Cynwyd": ["CYN"],
    "Norristown": ["NOR"],
    "Chestnut Hill West": ["CHW"],
    "Chestnut Hill East": ["CHE"],
    "Doylestown": ["GLN", "LAN"],
    "Lansdale": ["GLN", "LAN"],
    "Warminster": ["WAR"],
    "Glenside": ["GLN", "LAN", "WAR"],
    "West Trenton": ["WTR", "GLN"],
    "Fox Chase": ["FOX"],
    "North Philadelphia": ["CHW", "LAN", "TRE"],
    "Wawa": ["MED"],
    "Newark DE": ["WIL"],
    "Wilmington": ["WIL"],
    "Marcus Hook": ["WIL"],
    "Airport": ["AIR"],
    "Wayne Junction": ["CHE", "FOX", "GLN", "LAN", "WAR"],
    "Trenton": ["TRE"]
}