"""
SolarView - Interactive 2D Solar System Simulation in Python
Inspired by CogniSolver/solar-system
Created for Durgesh Patil (durgesh0314)
"""

import sys
import os
import pygame

# Local imports
from constants import (
    WINDOW_TITLE, DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT,
    FPS, COLOR_SPACE_BLACK, CELESTIAL_DATA, PLANET_KEYS
)
from starfield import Starfield
from celestial_body import CelestialBody
from camera import Camera
from ui import UI


class SolarSystemApp:
    def __init__(self, width=DEFAULT_WINDOW_WIDTH, height=DEFAULT_WINDOW_HEIGHT, headless=False):
        self.width = width
        self.height = height
        self.headless = headless
        self.running = True

        # Initialize Pygame
        pygame.init()
        pygame.display.set_caption(WINDOW_TITLE)

        if not self.headless:
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        else:
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.HIDDEN)

        self.clock = pygame.time.Clock()

        # Simulation states
        self.sim_speed = 1.0
        self.is_paused = False
        self.show_orbits = True
        self.show_trails = True
        self.show_labels = True

        # Asset Directory
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.asset_dir = os.path.join(base_dir, "assets", "images")

        # Initialize Subsystems
        self.starfield = Starfield(count=900, bounds=4500)
        self.camera = Camera(self.width, self.height)
        self.ui = UI(self.width, self.height)
        self.font_label = pygame.font.SysFont("Segoe UI, Arial, sans-serif", 12)

        # Build Celestial Hierarchy
        self.bodies = {}
        self._init_celestial_bodies()

        # Setup quick navigation buttons
        self.ui.setup_nav_bar(self.bodies, self.select_and_focus_body)

        # Hovered body tracking
        self.hovered_body = None

    def _init_celestial_bodies(self):
        """Create Sun, Planets, and the Moon with correct parentage."""
        # 1. Sun (Center)
        sun_data = CELESTIAL_DATA["sun"]
        self.sun = CelestialBody("sun", sun_data, self.asset_dir, parent=None)
        self.bodies["sun"] = self.sun

        # 2. Planets orbiting the Sun
        for key in PLANET_KEYS:
            if key in CELESTIAL_DATA:
                p_data = CELESTIAL_DATA[key]
                planet = CelestialBody(key, p_data, self.asset_dir, parent=self.sun)
                self.sun.add_child(planet)
                self.bodies[key] = planet

        # 3. Moon orbiting Earth
        if "earth" in self.bodies and "moon" in CELESTIAL_DATA:
            moon_data = CELESTIAL_DATA["moon"]
            moon = CelestialBody("moon", moon_data, self.asset_dir, parent=self.bodies["earth"])
            self.bodies["earth"].add_child(moon)
            self.bodies["moon"] = moon

    def select_and_focus_body(self, body):
        """Select a body, open its info card, and focus camera on it."""
        self.ui.selected_body = body
        self.camera.follow(body)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            elif event.type == pygame.VIDEORESIZE and not self.headless:
                self.width, self.height = event.w, event.h
                self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
                self.camera.resize(self.width, self.height)
                self.ui.resize(self.width, self.height, self.bodies, self.select_and_focus_body)

            # Let UI process first (navigation toolbar, close/follow buttons)
            if self.ui.handle_event(event, self.camera):
                continue

            # Mouse wheel for zoom
            if event.type == pygame.MOUSEWHEEL:
                mouse_pos = pygame.mouse.get_pos()
                if event.y > 0:
                    self.camera.zoom_at(mouse_pos, 1.15)
                elif event.y < 0:
                    self.camera.zoom_at(mouse_pos, 0.87)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    # Check if clicked on any body
                    clicked_body = None
                    for body in self.bodies.values():
                        if body.contains_point(event.pos[0], event.pos[1], self.camera):
                            clicked_body = body
                            break

                    if clicked_body is not None:
                        self.select_and_focus_body(clicked_body)
                    else:
                        self.camera.start_drag(event.pos)

                elif event.button == 4:  # Fallback wheel up
                    self.camera.zoom_at(event.pos, 1.15)
                elif event.button == 5:  # Fallback wheel down
                    self.camera.zoom_at(event.pos, 0.87)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.camera.end_drag()

            elif event.type == pygame.MOUSEMOTION:
                if self.camera.dragging:
                    self.camera.drag(event.pos)
                else:
                    # Update hover highlight
                    self.hovered_body = None
                    for body in self.bodies.values():
                        if body.contains_point(event.pos[0], event.pos[1], self.camera):
                            self.hovered_body = body
                            break

            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key)

    def _handle_keydown(self, key):
        if key == pygame.K_SPACE:
            self.is_paused = not self.is_paused
        elif key == pygame.K_UP:
            self.sim_speed = min(20.0, self.sim_speed + 0.25)
        elif key == pygame.K_DOWN:
            self.sim_speed = max(0.1, self.sim_speed - 0.25)
        elif key == pygame.K_r:
            self.camera.reset()
        elif key == pygame.K_f:
            if self.ui.selected_body:
                if self.camera.following == self.ui.selected_body:
                    self.camera.unfollow()
                else:
                    self.camera.follow(self.ui.selected_body)
        elif key == pygame.K_o:
            self.show_orbits = not self.show_orbits
        elif key == pygame.K_l:
            self.show_labels = not self.show_labels
        elif key == pygame.K_t:
            self.show_trails = not self.show_trails
        elif key == pygame.K_h:
            self.ui.show_help = not self.ui.show_help
        elif key == pygame.K_ESCAPE:
            if self.ui.show_help:
                self.ui.show_help = False
            elif self.ui.selected_body:
                self.ui.selected_body = None
                self.camera.unfollow()

        # Numeric hotkeys 0-9
        key_map = {
            pygame.K_0: "sun",
            pygame.K_1: "mercury",
            pygame.K_2: "venus",
            pygame.K_3: "earth",
            pygame.K_4: "moon",
            pygame.K_5: "mars",
            pygame.K_6: "jupiter",
            pygame.K_7: "saturn",
            pygame.K_8: "uranus",
            pygame.K_9: "neptune",
            pygame.K_p: "pluto"
        }
        if key in key_map and key_map[key] in self.bodies:
            self.select_and_focus_body(self.bodies[key_map[key]])

    def update(self, dt):
        self.starfield.update(dt)
        self.camera.update(dt)

        if not self.is_paused:
            self.sun.update(dt, self.sim_speed)

    def render(self):
        # 1. Clear background
        self.screen.fill(COLOR_SPACE_BLACK)

        # 2. Render deep space starfield & nebulae
        self.starfield.draw(self.screen, self.camera)

        # 3. Draw orbit paths
        if self.show_orbits:
            for body in self.bodies.values():
                body.draw_orbit(self.screen, self.camera)

        # 4. Draw orbital trails
        if self.show_trails:
            for body in self.bodies.values():
                body.draw_trail(self.screen, self.camera)

        # 5. Draw celestial bodies (ordered inside-out)
        ordered_draw_keys = ["sun", "mercury", "venus", "earth", "moon", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto"]
        for key in ordered_draw_keys:
            if key in self.bodies:
                body = self.bodies[key]
                is_sel = (self.ui.selected_body == body)
                is_hov = (self.hovered_body == body)
                body.draw(self.screen, self.camera, is_hovered=is_hov, is_selected=is_sel)

        # 6. Draw planet labels
        if self.show_labels:
            for body in self.bodies.values():
                body.draw_label(self.screen, self.camera, self.font_label)

        # 7. Draw UI and HUD Overlay
        self.ui.draw(
            self.screen, self.clock, self.sim_speed, self.is_paused,
            self.camera, self.show_orbits, self.show_trails, self.show_labels
        )

        if not self.headless:
            pygame.display.flip()

    def run(self, max_frames=None):
        frame_count = 0
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            dt = min(dt, 0.1)  # Clamp against delta-time spikes

            self.handle_events()
            self.update(dt)
            self.render()

            frame_count += 1
            if max_frames and frame_count >= max_frames:
                break

        pygame.quit()


def main():
    headless = "--test" in sys.argv or "--headless" in sys.argv
    max_frames = 90 if headless else None
    app = SolarSystemApp(headless=headless)
    app.run(max_frames=max_frames)
    if headless:
        print("Self-test completed successfully (90 frames rendered).")


if __name__ == "__main__":
    main()
