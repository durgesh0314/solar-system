"""
CelestialBody class representing the Sun, Planets, and Moons.
Handles physics, orbital revolution, self-rotation, rendering, trails, and interaction.
"""

import math
import os
from collections import deque
import pygame

class CelestialBody:
    def __init__(self, key, data, asset_dir, parent=None):
        self.key = key
        self.data = data
        self.name = data["name"]
        self.type_str = data.get("type", "Celestial Body")
        self.base_diameter = data["diameter"]
        self.orbit_radius = data["orbit_radius"]
        self.orbit_speed = data["orbit_speed"]
        self.rotation_speed = data["rotation_speed"]
        self.color = data.get("color", (200, 200, 200))
        self.info = data.get("info", {})
        self.parent = parent
        self.children = []

        # Dynamics state
        self.orbit_angle = 0.0
        self.rotation_angle = 0.0
        self.x = 0.0
        self.y = 0.0

        # Orbital trail (store world coordinates)
        self.trail = deque(maxlen=60)
        self.trail_timer = 0.0

        # Load and prepare texture
        texture_name = data.get("texture")
        self.raw_image = None
        if texture_name:
            path = os.path.join(asset_dir, texture_name)
            if os.path.exists(path):
                try:
                    loaded = pygame.image.load(path)
                    if pygame.display.get_surface() is not None:
                        try:
                            self.raw_image = loaded.convert_alpha()
                        except Exception:
                            self.raw_image = loaded
                    else:
                        self.raw_image = loaded
                except Exception as e:
                    print(f"Warning: Failed to load {path}: {e}")

        # Fallback surface if no texture loaded
        if self.raw_image is None:
            self.raw_image = pygame.Surface((self.base_diameter, self.base_diameter), pygame.SRCALPHA)
            pygame.draw.circle(
                self.raw_image,
                self.color,
                (self.base_diameter // 2, self.base_diameter // 2),
                self.base_diameter // 2
            )

        # Scale cache: zoom -> scaled surface
        self._cached_zoom = None
        self._cached_scaled_image = None
        self._cached_size = None

        # Sun corona animation state
        self.corona_pulse = 0.0

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def update(self, dt, speed_multiplier):
        # Update orbital revolution
        angular_velocity = self.orbit_speed * 0.5 * speed_multiplier
        self.orbit_angle = (self.orbit_angle + angular_velocity * dt) % (2.0 * math.pi)

        # Update self rotation
        self.rotation_angle = (self.rotation_angle + self.rotation_speed * 20.0 * speed_multiplier * dt) % 360.0

        # Update corona pulse if Sun
        if self.key == "sun":
            self.corona_pulse = (self.corona_pulse + 1.8 * dt) % (math.pi * 2)

        # Calculate world coordinates
        if self.parent is None:
            self.x = 0.0
            self.y = 0.0
        else:
            self.x = self.parent.x + math.cos(self.orbit_angle) * self.orbit_radius
            self.y = self.parent.y + math.sin(self.orbit_angle) * self.orbit_radius

        # Record trail point periodically
        self.trail_timer += dt
        if self.trail_timer >= 0.05:
            self.trail_timer = 0.0
            self.trail.append((self.x, self.y))

        # Recursively update children (e.g. Moon)
        for child in self.children:
            child.update(dt, speed_multiplier)

    def draw_orbit(self, surface, camera):
        """Draw circular orbit line around parent."""
        if self.parent is None or self.orbit_radius <= 0:
            return

        px, py = camera.world_to_screen(self.parent.x, self.parent.y)
        scaled_r = int(round(self.orbit_radius * camera.zoom))

        if scaled_r > 2:
            orbit_rect = pygame.Rect(px - scaled_r, py - scaled_r, scaled_r * 2, scaled_r * 2)
            # Only draw if visible on screen
            sw, sh = surface.get_size()
            if orbit_rect.colliderect(pygame.Rect(0, 0, sw, sh)):
                # Draw subtle orbit ring
                orbit_color = (
                    min(255, int(self.color[0] * 0.35 + 25)),
                    min(255, int(self.color[1] * 0.35 + 30)),
                    min(255, int(self.color[2] * 0.35 + 40))
                )
                pygame.draw.circle(surface, orbit_color, (px, py), scaled_r, width=1)

    def draw_trail(self, surface, camera):
        """Draw fading motion trail behind the planet."""
        if len(self.trail) < 2 or self.key == "sun":
            return

        num_points = len(self.trail)
        pts = [camera.world_to_screen(tx, ty) for tx, ty in self.trail]

        for i in range(num_points - 1):
            alpha_frac = (i + 1) / float(num_points)
            # Trail color fades from nearly black to planet color
            trail_col = (
                int(self.color[0] * alpha_frac * 0.7),
                int(self.color[1] * alpha_frac * 0.7),
                int(self.color[2] * alpha_frac * 0.7)
            )
            pygame.draw.line(surface, trail_col, pts[i], pts[i + 1], 1)

    def draw(self, surface, camera, is_hovered=False, is_selected=False):
        """Render body with texture rotation, corona, and selection rings."""
        sx, sy = camera.world_to_screen(self.x, self.y)
        sw, sh = surface.get_size()

        # Render Sun corona glow
        if self.key == "sun":
            self._draw_sun_corona(surface, sx, sy, camera.zoom)

        # Calculate current on-screen size (minimum 6px so far-away planets don't disappear)
        scaled_diameter = max(6, int(round(self.base_diameter * camera.zoom)))

        # Cache scaled texture
        if self._cached_scaled_image is None or self._cached_size != scaled_diameter:
            self._cached_scaled_image = pygame.transform.smoothscale(
                self.raw_image, (scaled_diameter, scaled_diameter)
            )
            self._cached_size = scaled_diameter

        # Rotate around its own axis
        # Invert rotation angle so it spins counter-clockwise (direct rotation)
        rotated_surf = pygame.transform.rotate(self._cached_scaled_image, -self.rotation_angle)
        rot_rect = rotated_surf.get_rect(center=(sx, sy))

        # Check visibility
        if rot_rect.colliderect(pygame.Rect(0, 0, sw, sh)):
            surface.blit(rotated_surf, rot_rect)

            # Draw day/night shading terminator on planets (dark side opposite Sun)
            if self.key != "sun" and scaled_diameter > 14:
                self._draw_shadow(surface, sx, sy, scaled_diameter // 2)

            # Selection / Hover highlight rings
            if is_selected:
                ring_r = scaled_diameter // 2 + 6
                pygame.draw.circle(surface, (255, 215, 0), (sx, sy), ring_r, width=2)
                # Outer indicator brackets
                pygame.draw.circle(surface, (255, 230, 100), (sx, sy), ring_r + 4, width=1)
            elif is_hovered:
                ring_r = scaled_diameter // 2 + 4
                pygame.draw.circle(surface, (120, 200, 255), (sx, sy), ring_r, width=1)

    def _draw_shadow(self, surface, sx, sy, radius):
        """Draw subtle 3D space lighting (shadow facing away from center)."""
        # Direction vector from Sun (center 0,0) to planet (self.x, self.y)
        angle_to_sun = math.atan2(self.y, self.x)
        shadow_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        # Create subtle crescent gradient on back side
        shadow_alpha = 110
        pygame.draw.circle(shadow_surf, (0, 0, 0, shadow_alpha), (radius, radius), radius)

        # Mask off the lit hemisphere
        lit_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        # Draw lit portion towards sun
        lit_center_x = radius - int(math.cos(angle_to_sun) * (radius * 0.45))
        lit_center_y = radius - int(math.sin(angle_to_sun) * (radius * 0.45))
        pygame.draw.circle(lit_surf, (255, 255, 255, 255), (lit_center_x, lit_center_y), int(radius * 1.1))

        # Combine
        shadow_surf.blit(lit_surf, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        surface.blit(shadow_surf, (sx - radius, sy - radius))

    def _draw_sun_corona(self, surface, sx, sy, zoom):
        """Dynamic pulsating solar corona with radiant orange/gold glow."""
        base_r = int(self.base_diameter * zoom / 2)
        pulse = 1.0 + 0.08 * math.sin(self.corona_pulse)
        max_corona_r = int((base_r + 45 * zoom) * pulse)

        if max_corona_r > 5:
            corona_surf = pygame.Surface((max_corona_r * 2, max_corona_r * 2), pygame.SRCALPHA)
            corona_center = (max_corona_r, max_corona_r)

            # Draw concentric soft radial glow layers
            layers = [
                (max_corona_r * 1.0, (255, 80, 0, 20)),
                (max_corona_r * 0.75, (255, 120, 10, 45)),
                (max_corona_r * 0.55, (255, 170, 30, 80)),
                (max_corona_r * 0.35, (255, 220, 80, 130)),
            ]
            for r, col in layers:
                pygame.draw.circle(corona_surf, col, corona_center, int(r))

            surface.blit(corona_surf, (sx - max_corona_r, sy - max_corona_r))

    def draw_label(self, surface, camera, font):
        """Render planet name label."""
        sx, sy = camera.world_to_screen(self.x, self.y)
        scaled_r = max(4, int(self.base_diameter * camera.zoom / 2))

        label_text = font.render(self.name, True, (215, 225, 240))
        label_rect = label_text.get_rect(center=(sx, sy + scaled_r + 12))

        # Draw subtle background pill for readability
        bg_rect = label_rect.inflate(8, 4)
        bg_surf = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        bg_surf.fill((10, 14, 24, 180))
        surface.blit(bg_surf, bg_rect.topleft)
        surface.blit(label_text, label_rect)

    def contains_point(self, screen_x, screen_y, camera):
        """Check if mouse coordinate intersects this celestial body."""
        sx, sy = camera.world_to_screen(self.x, self.y)
        radius = max(10, int(self.base_diameter * camera.zoom / 2))
        dist_sq = (screen_x - sx) ** 2 + (screen_y - sy) ** 2
        return dist_sq <= radius ** 2
