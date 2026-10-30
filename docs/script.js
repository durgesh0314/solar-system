// Celestial Data for Interactive Info Cards
const CELESTIAL_INFO = {
  sun: {
    name: "Sun",
    type: "Yellow Dwarf Star (G2V)",
    stats: {
      "Distance from Center": "0 AU (Center of System)",
      "Equatorial Diameter": "1,392,700 km",
      "Surface Temperature": "5,500 °C",
      "Mass": "1.989 × 10^30 kg (99.86% of Solar System)",
      "Rotation Period": "27 Earth days",
      "Fun Fact": "About 1.3 million Earths could fit inside the Sun!"
    }
  },
  mercury: {
    name: "Mercury",
    type: "Terrestrial Planet",
    stats: {
      "Distance from Sun": "0.39 AU (~57.9 million km)",
      "Equatorial Diameter": "4,879 km",
      "Orbital Period": "88 Earth days",
      "Rotation Period": "59 Earth days",
      "Moons": "0",
      "Surface Temp": "-180°C to 430°C",
      "Fun Fact": "Mercury has no atmosphere to trap heat, causing extreme swings!"
    }
  },
  venus: {
    name: "Venus",
    type: "Terrestrial Planet",
    stats: {
      "Distance from Sun": "0.72 AU (~108.2 million km)",
      "Equatorial Diameter": "12,104 km",
      "Orbital Period": "225 Earth days",
      "Rotation Period": "243 Earth days (Retrograde)",
      "Moons": "0",
      "Surface Temp": "465°C (Hottest in Solar System)",
      "Fun Fact": "Venus rotates backwards compared to most other planets!"
    }
  },
  earth: {
    name: "Earth",
    type: "Terrestrial Planet (Oasis of Life)",
    stats: {
      "Distance from Sun": "1.00 AU (~149.6 million km)",
      "Equatorial Diameter": "12,742 km",
      "Orbital Period": "365.25 Earth days",
      "Rotation Period": "23.9 Hours",
      "Moons": "1 (The Moon / Luna)",
      "Atmosphere": "78% Nitrogen, 21% Oxygen",
      "Fun Fact": "Earth is the only known planet harboring life and liquid water!"
    }
  },
  moon: {
    name: "The Moon",
    type: "Natural Satellite (Luna)",
    stats: {
      "Parent Body": "Earth",
      "Distance from Earth": "384,400 km",
      "Diameter": "3,474 km",
      "Orbital Period": "27.3 Earth days",
      "Tidal Locking": "Yes (Same face always points to Earth)",
      "Fun Fact": "The Moon's gravitational pull creates the ocean tides on Earth."
    }
  },
  mars: {
    name: "Mars",
    type: "Terrestrial Planet (The Red Planet)",
    stats: {
      "Distance from Sun": "1.52 AU (~227.9 million km)",
      "Equatorial Diameter": "6,779 km",
      "Orbital Period": "687 Earth days",
      "Rotation Period": "24.6 Hours",
      "Moons": "2 (Phobos, Deimos)",
      "Highest Peak": "Olympus Mons (21.9 km high volcano)",
      "Fun Fact": "Mars appears red due to iron oxide (rust) on its surface."
    }
  },
  jupiter: {
    name: "Jupiter",
    type: "Gas Giant (King of Planets)",
    stats: {
      "Distance from Sun": "5.20 AU (~778.5 million km)",
      "Equatorial Diameter": "139,820 km (Largest Planet)",
      "Orbital Period": "11.86 Earth years",
      "Rotation Period": "9.9 Hours (Fastest rotation)",
      "Moons": "95 confirmed moons",
      "Fun Fact": "Jupiter has a mass 2.5 times all other planets combined!"
    }
  },
  saturn: {
    name: "Saturn",
    type: "Gas Giant (Ringed Wonder)",
    stats: {
      "Distance from Sun": "9.58 AU (~1.43 billion km)",
      "Equatorial Diameter": "116,460 km",
      "Orbital Period": "29.45 Earth years",
      "Rotation Period": "10.7 Hours",
      "Moons": "146 confirmed moons (Titan is largest)",
      "Fun Fact": "Saturn is less dense than water; it would float in a giant bathtub!"
    }
  },
  uranus: {
    name: "Uranus",
    type: "Ice Giant",
    stats: {
      "Distance from Sun": "19.22 AU (~2.87 billion km)",
      "Equatorial Diameter": "50,724 km",
      "Orbital Period": "84 Earth years",
      "Rotation Period": "17.2 Hours (Sideways spin 98° tilt)",
      "Moons": "28 known moons",
      "Fun Fact": "Uranus rotates on its side, rolling like a ball around the Sun!"
    }
  },
  neptune: {
    name: "Neptune",
    type: "Ice Giant (Windy World)",
    stats: {
      "Distance from Sun": "30.05 AU (~4.50 billion km)",
      "Equatorial Diameter": "49,244 km",
      "Orbital Period": "164.8 Earth years",
      "Rotation Period": "16.1 Hours",
      "Moons": "16 known moons",
      "Fun Fact": "Neptune has the fastest supersonic winds in the solar system (>2,100 km/h)!"
    }
  },
  pluto: {
    name: "Pluto",
    type: "Dwarf Planet (Kuiper Belt Object)",
    stats: {
      "Distance from Sun": "39.48 AU (~5.91 billion km)",
      "Equatorial Diameter": "2,376 km",
      "Orbital Period": "248 Earth years",
      "Rotation Period": "6.4 Earth days",
      "Moons": "5 (Charon, Styx, Nix, Kerberos, Hydra)",
      "Fun Fact": "Pluto features a giant heart-shaped nitrogen glacier named Tombaugh Regio."
    }
  }
};

// Generate 1000 Deep Space Stars
function createStars() {
  const body = document.querySelector("body");
  const starCount = 1000;
  const fragment = document.createDocumentFragment();

  for (let i = 0; i < starCount; i++) {
    const star = document.createElement("div");
    star.className = "star";
    const size = Math.random() < 0.15 ? (Math.random() * 1.5 + 1.2) : (Math.random() * 0.8 + 0.4);
    star.style.width = `${size}px`;
    star.style.height = `${size}px`;
    star.style.top = `${Math.random() * 100}%`;
    star.style.left = `${Math.random() * 100}%`;
    star.style.opacity = (Math.random() * 0.7 + 0.3).toFixed(2);
    fragment.appendChild(star);
  }
  body.appendChild(fragment);
}

// Info Card Interaction
const infoModal = document.getElementById("info-modal");
const cardName = document.getElementById("card-name");
const cardType = document.getElementById("card-type");
const cardDetails = document.getElementById("card-details");
const closeCardBtn = document.getElementById("close-card");

function showPlanetInfo(planetKey) {
  const data = CELESTIAL_INFO[planetKey];
  if (!data) return;

  cardName.textContent = data.name;
  cardType.textContent = data.type;
  cardDetails.innerHTML = "";

  for (const [key, val] of Object.entries(data.stats)) {
    const row = document.createElement("div");
    row.className = "card-row";
    row.innerHTML = `<div class="label">${key}</div><div class="value">${val}</div>`;
    cardDetails.appendChild(row);
  }

  infoModal.classList.remove("hidden");
}

function hidePlanetInfo() {
  infoModal.classList.add("hidden");
}

// Event Listeners for Planet Clicking
document.querySelectorAll(".planet-node").forEach(node => {
  node.addEventListener("click", (e) => {
    e.stopPropagation();
    const planetKey = node.getAttribute("data-planet");
    showPlanetInfo(planetKey);
  });
});

document.querySelectorAll(".nav-chip").forEach(btn => {
  btn.addEventListener("click", (e) => {
    e.stopPropagation();
    const planetKey = btn.getAttribute("data-planet");
    showPlanetInfo(planetKey);
  });
});

closeCardBtn.addEventListener("click", hidePlanetInfo);

// Simulation Controls
const pauseBtn = document.getElementById("pause-btn");
const speedSlider = document.getElementById("speed-slider");
const speedLabel = document.getElementById("speed-label");
const zoomInBtn = document.getElementById("zoom-in");
const zoomOutBtn = document.getElementById("zoom-out");
const zoomResetBtn = document.getElementById("zoom-reset");

let isPaused = false;
let currentZoom = 1.0;

pauseBtn.addEventListener("click", () => {
  isPaused = !isPaused;
  document.body.classList.toggle("paused", isPaused);
  pauseBtn.textContent = isPaused ? "▶️ Resume" : "⏸️ Pause";
});

speedSlider.addEventListener("input", (e) => {
  const speed = parseFloat(e.target.value);
  document.documentElement.style.setProperty("--sim-speed", speed);
  speedLabel.textContent = `${speed.toFixed(1)}x`;
});

function applyZoom(delta) {
  currentZoom = Math.min(2.5, Math.max(0.4, currentZoom + delta));
  document.documentElement.style.setProperty("--zoom-level", currentZoom);
}

zoomInBtn.addEventListener("click", () => applyZoom(0.15));
zoomOutBtn.addEventListener("click", () => applyZoom(-0.15));
zoomResetBtn.addEventListener("click", () => {
  currentZoom = 1.0;
  document.documentElement.style.setProperty("--zoom-level", currentZoom);
});

// Initialize
createStars();
