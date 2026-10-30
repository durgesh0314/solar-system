"""
Deep space starfield with multi-layer parallax, twinkling stars, and faint cosmic nebula glow.
"""

import math
import random
import pygame

class Starfield:
    def __init__(self, count=900, bounds=4000):
        self.bounds = bounds
        self.stars = []
        random.seed(42)

        # Pre-generate stars across large bounds
        # (x, y, depth, base_radius, base_brightness, twinkle_speed, twinkle_phase, color)
        for _ in range(count):
            x = random.uniform(-bounds / 2, bounds / 2)
            y = random.uniform(-bounds / 2, bounds / 2)
            depth = random.choice([0.15, 0.35, 0.65, 0.95])  # Parallax depth factor
            base_r = 1 if depth < 0.5 else (2 if random.random() < 0.25 else 1)
            brightness = random.randint(120, 255)
            twinkle_speed = random.uniform(1.5, 4.5)
            phase = random.uniform(0, math.pi * 2)

            # Realistic star color distribution
            c_rand = random.random()
            if c_rand < 0.70:
                color = (255, 255, 255)
            elif c_rand < 0.85:
                color = (200, 220, 255)  # Blue-white
            elif c_rand < 0.95:
                color = (255, 235, 190)  # Pale yellow
            else:
                color = (255, 190, 180)  # Pale orange/red

            self.stars.append([x, y, depth, base_r, brightness, twinkle_speed, phase, color])

        # Pre-render faint nebulae surfaces for high performance
        self.nebulae = []
        self._init_nebulae()

    def _init_nebulae(self):
        nebula_colors = [
            (25, 15, 45, 18),   # Purple/violet haze
            (10, 25, 40, 16),   # Deep cyan haze
            (35, 15, 20, 14),   # Crimson/magenta haze
            (15, 30, 25, 15)    # Emerald/teal haze
        ]
        nebula_positions = [
            (-600, -500, 500),
            (700, 450, 600),
            (-800, 600, 550),
            (850, -650, 480)
        ]

        for (wx, wy, radius), col in zip(nebula_positions, nebula_colors):
            surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            steps = 12
            for i in range(steps, 0, -1):
                r = int(radius * (i / steps))
                alpha = int(col[3] * (1.0 - (i / steps) ** 1.5))
                pygame.draw.circle(surf, (col[0], col[1], col[2], alpha), (radius, radius), r)
            self.nebulae.append((wx, wy, radius, surf))

    def update(self, dt):
        for star in self.stars:
            star[6] += star[5] * dt

    def draw(self, surface, camera):
        w, h = surface.get_size()
        cam_x, cam_y = camera.x, camera.y
        zoom = camera.zoom

        # 1. Draw nebulae with parallax
        for wx, wy, radius, neb_surf in self.nebulae:
            depth = 0.08  # Very distant
            sx = int((wx - cam_x * depth) * zoom + w / 2 - radius * zoom)
            sy = int((wy - cam_y * depth) * zoom + h / 2 - radius * zoom)
            scaled_size = int(radius * 2 * zoom)
            if -scaled_size < sx < w and -scaled_size < sy < h:
                if abs(zoom - 1.0) > 0.05:
                    s = pygame.transform.smoothscale(neb_surf, (scaled_size, scaled_size))
                    surface.blit(s, (sx, sy))
                else:
                    surface.blit(neb_surf, (sx, sy))

        # 2. Draw stars
        half_b = self.bounds / 2
        for x, y, depth, r, base_bright, speed, phase, color in self.stars:
            # Parallax calculation
            eff_x = (x - cam_x * depth)
            eff_y = (y - cam_y * depth)

            # Wrap around boundaries so the sky is infinite
            eff_x = (eff_x + half_b) % self.bounds - half_b
            eff_y = (eff_y + half_b) % self.bounds - half_b

            # Screen projection
            sx = int(eff_x * (0.6 + 0.4 * depth) + w / 2)
            sy = int(eff_y * (0.6 + 0.4 * depth) + h / 2)

            if 0 <= sx < w and 0 <= sy < h:
                # Twinkle alpha calculation using phase sine
                twinkle = 0.7 + 0.3 * math.sin(phase)
                bright = min(255, max(30, int(base_bright * twinkle)))
                star_color = (
                    min(255, int(color[0] * bright / 255)),
                    min(255, int(color[1] * bright / 255)),
                    min(255, int(color[2] * bright / 255))
                )

                if r == 1:
                    surface.set_at((sx, sy), star_color)
                else:
                    pygame.draw.circle(surface, star_color, (sx, sy), r)
