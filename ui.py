"""
UI and HUD overlay module for SolarView simulation.
Renders celestial info cards, control guides, timeline speed HUD, and quick navigation bar.
"""

import pygame

class Button:
    def __init__(self, rect, text, callback, bg_color=(25, 35, 55, 200), hover_color=(45, 65, 105, 220)):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.is_hovered = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()
                return True
        return False

    def draw(self, surface, font):
        bg = self.hover_color if self.is_hovered else self.bg_color
        btn_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        btn_surf.fill(bg)
        surface.blit(btn_surf, self.rect.topleft)

        border_col = (100, 150, 220) if self.is_hovered else (60, 80, 120)
        pygame.draw.rect(surface, border_col, self.rect, width=1, border_radius=4)

        text_surf = font.render(self.text, True, (240, 245, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)


class UI:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.show_help = False
        self.selected_body = None

        # Fonts
        pygame.font.init()
        self.font_title = pygame.font.SysFont("Segoe UI, Arial, sans-serif", 20, bold=True)
        self.font_heading = pygame.font.SysFont("Segoe UI, Arial, sans-serif", 16, bold=True)
        self.font_body = pygame.font.SysFont("Segoe UI, Arial, sans-serif", 13)
        self.font_small = pygame.font.SysFont("Segoe UI, Arial, sans-serif", 11)

        # Quick navigation bar buttons
        self.nav_buttons = []
        self.close_btn = None
        self.follow_btn = None

    def resize(self, width, height, bodies_dict=None, on_select_cb=None):
        self.screen_width = width
        self.screen_height = height
        if bodies_dict and on_select_cb:
            self.setup_nav_bar(bodies_dict, on_select_cb)

    def setup_nav_bar(self, bodies_dict, on_select_cb):
        """Create bottom quick-jump toolbar for all celestial bodies."""
        self.nav_buttons = []
        ordered_keys = ["sun", "mercury", "venus", "earth", "moon", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto"]
        btn_w = 68
        btn_h = 26
        gap = 5
        total_w = len(ordered_keys) * btn_w + (len(ordered_keys) - 1) * gap
        start_x = max(10, (self.screen_width - total_w) // 2)
        start_y = self.screen_height - 38

        for i, key in enumerate(ordered_keys):
            if key in bodies_dict:
                body = bodies_dict[key]
                rect = (start_x + i * (btn_w + gap), start_y, btn_w, btn_h)
                btn = Button(
                    rect=rect,
                    text=body.name,
                    callback=lambda b=body: on_select_cb(b)
                )
                self.nav_buttons.append(btn)

    def handle_event(self, event, camera):
        # Check nav buttons
        for btn in self.nav_buttons:
            if btn.handle_event(event):
                return True

        # Check info card buttons
        if self.selected_body:
            if self.close_btn and self.close_btn.handle_event(event):
                self.selected_body = None
                return True
            if self.follow_btn and self.follow_btn.handle_event(event):
                if camera.following == self.selected_body:
                    camera.unfollow()
                else:
                    camera.follow(self.selected_body)
                return True

        return False

    def draw(self, surface, clock, sim_speed, is_paused, camera, orbits_on, trails_on, labels_on):
        sw, sh = self.screen_width, self.screen_height

        # 1. Top HUD Bar
        self._draw_top_bar(surface, clock, sim_speed, is_paused, camera, orbits_on, trails_on, labels_on)

        # 2. Bottom Quick Navigation Bar
        for btn in self.nav_buttons:
            btn.draw(surface, self.font_small)

        # 3. Selected Body Info Card (Right Side)
        if self.selected_body:
            self._draw_info_card(surface, camera)

        # 4. Help Overlay (if active)
        if self.show_help:
            self._draw_help_overlay(surface)

    def _draw_top_bar(self, surface, clock, sim_speed, is_paused, camera, orbits_on, trails_on, labels_on):
        bar_h = 44
        bar_surf = pygame.Surface((self.screen_width, bar_h), pygame.SRCALPHA)
        bar_surf.fill((10, 14, 25, 210))
        surface.blit(bar_surf, (0, 0))
        pygame.draw.line(surface, (40, 55, 85), (0, bar_h), (self.screen_width, bar_h), 1)

        # Title
        title_surf = self.font_title.render("SolarView  ", True, (255, 215, 0))
        sub_surf = self.font_body.render("Python Edition", True, (130, 160, 210))
        surface.blit(title_surf, (15, 8))
        surface.blit(sub_surf, (15 + title_surf.get_width(), 13))

        # Simulation Speed & Status
        fps = int(clock.get_fps())
        pause_str = "[PAUSED]" if is_paused else "[RUNNING]"
        pause_col = (255, 90, 90) if is_paused else (80, 230, 130)

        status_text = f"Speed: {sim_speed:.1f}x  |  FPS: {fps}  |  Zoom: {camera.zoom:.2f}x"
        stat_surf = self.font_body.render(status_text, True, (200, 210, 230))
        pause_surf = self.font_body.render(pause_str, True, pause_col)

        surface.blit(pause_surf, (310, 12))
        surface.blit(stat_surf, (310 + pause_surf.get_width() + 15, 12))

        # Active Toggles Status
        toggles = f"Orbits: {'ON' if orbits_on else 'OFF'} [O] | Trails: {'ON' if trails_on else 'OFF'} [T] | Labels: {'ON' if labels_on else 'OFF'} [L] | Help: [H]"
        tog_surf = self.font_small.render(toggles, True, (150, 170, 200))
        surface.blit(tog_surf, (self.screen_width - tog_surf.get_width() - 15, 15))

    def _draw_info_card(self, surface, camera):
        card_w = 320
        card_h = min(460, self.screen_height - 110)
        card_x = self.screen_width - card_w - 20
        card_y = 56

        # Translucent Background Panel
        panel = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
        panel.fill((12, 17, 30, 235))
        surface.blit(panel, (card_x, card_y))
        pygame.draw.rect(surface, (65, 90, 140), (card_x, card_y, card_w, card_h), width=1, border_radius=8)

        # Header with Body Color Indicator
        color_dot_r = 7
        pygame.draw.circle(surface, self.selected_body.color, (card_x + 22, card_y + 24), color_dot_r)
        name_surf = self.font_heading.render(self.selected_body.name, True, (255, 255, 255))
        surface.blit(name_surf, (card_x + 36, card_y + 14))

        type_surf = self.font_small.render(self.selected_body.type_str, True, (140, 175, 220))
        surface.blit(type_surf, (card_x + 36, card_y + 34))

        # Separator line
        pygame.draw.line(surface, (45, 60, 95), (card_x + 15, card_y + 54), (card_x + card_w - 15, card_y + 54), 1)

        # Action Buttons
        is_following = (camera.following == self.selected_body)
        follow_text = "Unfollow" if is_following else "Follow Camera"
        self.follow_btn = Button(
            rect=(card_x + 15, card_y + 62, 135, 24),
            text=follow_text,
            callback=lambda: None,
            bg_color=(35, 50, 85, 220)
        )
        self.close_btn = Button(
            rect=(card_x + card_w - 75, card_y + 62, 60, 24),
            text="Close",
            callback=lambda: None,
            bg_color=(55, 30, 35, 220)
        )
        self.follow_btn.draw(surface, self.font_small)
        self.close_btn.draw(surface, self.font_small)

        # Info Items Grid
        curr_y = card_y + 98
        info_items = list(self.selected_body.info.items())
        for k, v in info_items:
            if curr_y > card_y + card_h - 25:
                break
            lbl_surf = self.font_small.render(k, True, (130, 150, 180))
            surface.blit(lbl_surf, (card_x + 15, curr_y))

            # Value text wrapping if long (e.g. Fun Fact)
            val_words = str(v).split(' ')
            line = ""
            lines = []
            for word in val_words:
                test_line = line + word + " "
                if self.font_body.size(test_line)[0] < (card_w - 30):
                    line = test_line
                else:
                    lines.append(line)
                    line = word + " "
            lines.append(line)

            for l_idx, l_str in enumerate(lines):
                val_surf = self.font_body.render(l_str.strip(), True, (240, 245, 255))
                surface.blit(val_surf, (card_x + 15, curr_y + 14 + l_idx * 16))

            curr_y += 18 + len(lines) * 16

    def _draw_help_overlay(self, surface):
        box_w = 460
        box_h = 440
        box_x = (self.screen_width - box_w) // 2
        box_y = (self.screen_height - box_h) // 2

        # Dim background
        dim_surf = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        dim_surf.fill((0, 0, 0, 160))
        surface.blit(dim_surf, (0, 0))

        # Panel
        panel = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        panel.fill((16, 22, 38, 250))
        surface.blit(panel, (box_x, box_y))
        pygame.draw.rect(surface, (80, 115, 180), (box_x, box_y, box_w, box_h), width=2, border_radius=10)

        # Title
        t_surf = self.font_heading.render("Controls & Navigation Guide", True, (255, 215, 0))
        surface.blit(t_surf, (box_x + 20, box_y + 18))

        guide = [
            ("Left Click + Drag", "Pan the cosmic view"),
            ("Mouse Wheel", "Zoom in / out smoothly"),
            ("Left Click Planet", "Inspect planet facts & info card"),
            ("Spacebar", "Pause / Resume simulation"),
            ("Up / Down Arrow", "Speed up / slow down time"),
            ("R Key", "Reset camera view (Center on Sun)"),
            ("F Key", "Toggle follow camera on selected planet"),
            ("O Key", "Toggle orbit lines on / off"),
            ("L Key", "Toggle planet name labels"),
            ("T Key", "Toggle orbital movement trails"),
            ("0 Key", "Quick jump to Sun"),
            ("1 - 9 Keys", "Quick jump: Mercury, Venus, Earth..."),
            ("H Key / ESC", "Close this controls guide")
        ]

        curr_y = box_y + 55
        for key_str, desc_str in guide:
            k_surf = self.font_body.render(key_str, True, (110, 190, 255))
            d_surf = self.font_body.render(desc_str, True, (220, 225, 240))
            surface.blit(k_surf, (box_x + 25, curr_y))
            surface.blit(d_surf, (box_x + 195, curr_y))
            curr_y += 24

        close_hint = self.font_small.render("Press 'H' or 'ESC' to dismiss", True, (130, 145, 175))
        surface.blit(close_hint, (box_x + (box_w - close_hint.get_width()) // 2, box_y + box_h - 26))
