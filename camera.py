"""
Camera module for 2D pan, zoom, and target tracking.
"""

class Camera:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.target_x = 0.0
        self.target_y = 0.0
        self.x = 0.0
        self.y = 0.0
        self.target_zoom = 0.85
        self.zoom = 0.85
        self.min_zoom = 0.15
        self.max_zoom = 4.5
        self.following = None  # Reference to a CelestialBody
        self.dragging = False
        self.drag_start = (0, 0)
        self.drag_start_cam = (0.0, 0.0)

    def resize(self, width, height):
        self.screen_width = width
        self.screen_height = height

    def follow(self, body):
        self.following = body

    def unfollow(self):
        self.following = None

    def reset(self):
        self.following = None
        self.target_x = 0.0
        self.target_y = 0.0
        self.target_zoom = 0.85

    def update(self, dt):
        if self.following is not None:
            # Follow target body
            self.target_x = self.following.x
            self.target_y = self.following.y

        # Smooth camera lerping
        lerp_factor = min(1.0, 10.0 * dt)
        self.x += (self.target_x - self.x) * lerp_factor
        self.y += (self.target_y - self.y) * lerp_factor
        self.zoom += (self.target_zoom - self.zoom) * lerp_factor

    def world_to_screen(self, wx, wy):
        sx = (wx - self.x) * self.zoom + self.screen_width / 2.0
        sy = (wy - self.y) * self.zoom + self.screen_height / 2.0
        return int(round(sx)), int(round(sy))

    def screen_to_world(self, sx, sy):
        wx = (sx - self.screen_width / 2.0) / self.zoom + self.x
        wy = (sy - self.screen_height / 2.0) / self.zoom + self.y
        return wx, wy

    def start_drag(self, mouse_pos):
        self.dragging = True
        self.drag_start = mouse_pos
        self.drag_start_cam = (self.target_x, self.target_y)
        self.following = None

    def drag(self, mouse_pos):
        if self.dragging:
            dx = (mouse_pos[0] - self.drag_start[0]) / self.zoom
            dy = (mouse_pos[1] - self.drag_start[1]) / self.zoom
            self.target_x = self.drag_start_cam[0] - dx
            self.target_y = self.drag_start_cam[1] - dy
            self.x = self.target_x
            self.y = self.target_y

    def end_drag(self):
        self.dragging = False

    def zoom_at(self, mouse_pos, factor):
        # Zoom centered at mouse position
        old_zoom = self.target_zoom
        new_zoom = max(self.min_zoom, min(self.max_zoom, old_zoom * factor))
        if new_zoom == old_zoom:
            return

        # Keep world position under mouse steady
        wx, wy = self.screen_to_world(*mouse_pos)
        self.target_zoom = new_zoom
        self.target_x = wx - (mouse_pos[0] - self.screen_width / 2.0) / new_zoom
        self.target_y = wy - (mouse_pos[1] - self.screen_height / 2.0) / new_zoom
