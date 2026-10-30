"""
Constants and celestial data for the Solar System simulation.
Inspired by CogniSolver/solar-system and enhanced for Python & Pygame.
"""

import math

# Window and Rendering settings
WINDOW_TITLE = "SolarView - Interactive 2D Solar System Simulation"
DEFAULT_WINDOW_WIDTH = 1366
DEFAULT_WINDOW_HEIGHT = 768
FPS = 60

# Color Palette (RGB)
COLOR_SPACE_BLACK = (5, 5, 12)
COLOR_WHITE = (255, 255, 255)
COLOR_ORBIT_DEFAULT = (45, 55, 75)
COLOR_ORBIT_ACTIVE = (120, 150, 220)
COLOR_TEXT_PRIMARY = (235, 240, 255)
COLOR_TEXT_SECONDARY = (160, 175, 205)
COLOR_TEXT_ACCENT = (255, 190, 70)
COLOR_PANEL_BG = (12, 16, 28, 220)
COLOR_PANEL_BORDER = (50, 70, 110, 200)

# Celestial Bodies Configuration
# Keys: name, texture, base_diameter, orbit_radius, speed_factor, rotation_speed, info
CELESTIAL_DATA = {
    "sun": {
        "name": "Sun",
        "type": "Yellow Dwarf Star (G2V)",
        "texture": "sun.png",
        "diameter": 76,
        "orbit_radius": 0,
        "orbit_speed": 0.0,
        "rotation_speed": 0.25,
        "color": (255, 180, 40),
        "info": {
            "Distance from Center": "0 AU (Center of System)",
            "Equatorial Diameter": "1,392,700 km",
            "Surface Temperature": "5,500 °C",
            "Mass": "1.989 × 10^30 kg (99.86% of system)",
            "Rotation Period": "27 Earth days",
            "Classification": "G-type main-sequence star",
            "Fun Fact": "About 1.3 million Earths could fit inside the Sun!"
        }
    },
    "mercury": {
        "name": "Mercury",
        "type": "Terrestrial Planet",
        "texture": "mercury.png",
        "diameter": 18,
        "orbit_radius": 75,
        "orbit_speed": 1.60,
        "rotation_speed": 0.3,
        "color": (169, 153, 140),
        "info": {
            "Distance from Sun": "0.39 AU (~57.9 million km)",
            "Equatorial Diameter": "4,879 km",
            "Orbital Period": "88 Earth days",
            "Rotation Period": "59 Earth days",
            "Moons": "0",
            "Surface Temp": "-180°C to 430°C",
            "Fun Fact": "Mercury has no atmosphere to trap heat, causing extreme swings!"
        }
    },
    "venus": {
        "name": "Venus",
        "type": "Terrestrial Planet",
        "texture": "venus.png",
        "diameter": 24,
        "orbit_radius": 120,
        "orbit_speed": 1.18,
        "rotation_speed": -0.2,
        "color": (227, 187, 118),
        "info": {
            "Distance from Sun": "0.72 AU (~108.2 million km)",
            "Equatorial Diameter": "12,104 km",
            "Orbital Period": "225 Earth days",
            "Rotation Period": "243 Earth days (Retrograde)",
            "Moons": "0",
            "Surface Temp": "465°C (Hottest in Solar System)",
            "Fun Fact": "Venus rotates backwards compared to most other planets!"
        }
    },
    "earth": {
        "name": "Earth",
        "type": "Terrestrial Planet (Oasis of Life)",
        "texture": "earth.png",
        "diameter": 28,
        "orbit_radius": 180,
        "orbit_speed": 1.00,
        "rotation_speed": 0.8,
        "color": (90, 160, 240),
        "info": {
            "Distance from Sun": "1.00 AU (~149.6 million km)",
            "Equatorial Diameter": "12,742 km",
            "Orbital Period": "365.25 Earth days (1 Year)",
            "Rotation Period": "23.9 Hours",
            "Moons": "1 (The Moon / Luna)",
            "Atmosphere": "78% Nitrogen, 21% Oxygen",
            "Fun Fact": "Earth is the only known planet harboring life and liquid water!"
        }
    },
    "moon": {
        "name": "Moon",
        "type": "Natural Satellite (Luna)",
        "texture": "moon.png",
        "diameter": 10,
        "orbit_radius": 28,  # Relative to Earth
        "orbit_speed": 4.5,
        "rotation_speed": 4.5,  # Tidally locked
        "color": (200, 200, 205),
        "info": {
            "Parent Body": "Earth",
            "Distance from Earth": "384,400 km",
            "Diameter": "3,474 km",
            "Orbital Period": "27.3 Earth days",
            "Tidal Locking": "Yes (Same face always points to Earth)",
            "Fun Fact": "The Moon causes the ocean tides on Earth."
        }
    },
    "mars": {
        "name": "Mars",
        "type": "Terrestrial Planet (The Red Planet)",
        "texture": "mars.png",
        "diameter": 20,
        "orbit_radius": 240,
        "orbit_speed": 0.80,
        "rotation_speed": 0.75,
        "color": (214, 98, 65),
        "info": {
            "Distance from Sun": "1.52 AU (~227.9 million km)",
            "Equatorial Diameter": "6,779 km",
            "Orbital Period": "687 Earth days",
            "Rotation Period": "24.6 Hours",
            "Moons": "2 (Phobos, Deimos)",
            "Highest Peak": "Olympus Mons (21.9 km high volcano)",
            "Fun Fact": "Mars appears red due to iron oxide (rust) on its surface."
        }
    },
    "jupiter": {
        "name": "Jupiter",
        "type": "Gas Giant (King of Planets)",
        "texture": "jupiter.png",
        "diameter": 54,
        "orbit_radius": 320,
        "orbit_speed": 0.44,
        "rotation_speed": 1.2,
        "color": (211, 166, 126),
        "info": {
            "Distance from Sun": "5.20 AU (~778.5 million km)",
            "Equatorial Diameter": "139,820 km (Largest Planet)",
            "Orbital Period": "11.86 Earth years",
            "Rotation Period": "9.9 Hours (Fastest rotation)",
            "Moons": "95 confirmed moons",
            "Notable Feature": "Great Red Spot (Century-old storm)",
            "Fun Fact": "Jupiter has a mass 2.5 times all other planets combined!"
        }
    },
    "saturn": {
        "name": "Saturn",
        "type": "Gas Giant (Ringed Wonder)",
        "texture": "saturn.png",
        "diameter": 48,
        "orbit_radius": 410,
        "orbit_speed": 0.32,
        "rotation_speed": 1.1,
        "color": (230, 205, 140),
        "info": {
            "Distance from Sun": "9.58 AU (~1.43 billion km)",
            "Equatorial Diameter": "116,460 km",
            "Orbital Period": "29.45 Earth years",
            "Rotation Period": "10.7 Hours",
            "Moons": "146 confirmed moons (Titan is largest)",
            "Rings": "Composed of 99% water ice and rock dust",
            "Fun Fact": "Saturn is less dense than water; it would float in a giant bathtub!"
        }
    },
    "uranus": {
        "name": "Uranus",
        "type": "Ice Giant",
        "texture": "uranus.png",
        "diameter": 32,
        "orbit_radius": 500,
        "orbit_speed": 0.23,
        "rotation_speed": -0.6,
        "color": (150, 220, 225),
        "info": {
            "Distance from Sun": "19.22 AU (~2.87 billion km)",
            "Equatorial Diameter": "50,724 km",
            "Orbital Period": "84 Earth years",
            "Rotation Period": "17.2 Hours (Sideways spin 98° tilt)",
            "Moons": "28 known moons",
            "Atmosphere": "Hydrogen, Helium, and Methane",
            "Fun Fact": "Uranus rotates on its side, rolling like a ball around the Sun!"
        }
    },
    "neptune": {
        "name": "Neptune",
        "type": "Ice Giant (Windy World)",
        "texture": "neptune.png",
        "diameter": 32,
        "orbit_radius": 590,
        "orbit_speed": 0.18,
        "rotation_speed": 0.7,
        "color": (75, 115, 230),
        "info": {
            "Distance from Sun": "30.05 AU (~4.50 billion km)",
            "Equatorial Diameter": "49,244 km",
            "Orbital Period": "164.8 Earth years",
            "Rotation Period": "16.1 Hours",
            "Moons": "16 known moons (Triton orbits backwards)",
            "Winds": "Over 2,100 km/h (Fastest in Solar System)",
            "Fun Fact": "Neptune was discovered through mathematical prediction before telescope sighting!"
        }
    },
    "pluto": {
        "name": "Pluto",
        "type": "Dwarf Planet (Kuiper Belt Object)",
        "texture": "pluto.png",
        "diameter": 16,
        "orbit_radius": 680,
        "orbit_speed": 0.15,
        "rotation_speed": 0.3,
        "color": (195, 175, 160),
        "info": {
            "Distance from Sun": "39.48 AU (~5.91 billion km)",
            "Equatorial Diameter": "2,376 km",
            "Orbital Period": "248 Earth years",
            "Rotation Period": "153.3 Hours (6.4 Earth days)",
            "Moons": "5 (Charon, Styx, Nix, Kerberos, Hydra)",
            "Surface Feature": "Tombaugh Regio (Giant heart-shaped nitrogen glacier)",
            "Fun Fact": "Pluto's largest moon Charon is so big they orbit a point outside Pluto!"
        }
    }
}

# Ordered list of body keys from inside out
PLANET_KEYS = ["mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto"]
