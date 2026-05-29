class Settings():
    """Settings class"""
    def __init__(self) -> None:
        self.load_settings()

    def load_settings(self):
        self.fps = 120
        self.window_width = 1280
        self.window_height = 720

        self.volume = 0.7

        self.difficulty = 'easy'
        self._apply_difficulty()

    def set_difficulty(self, level):
        self.difficulty = level
        self._apply_difficulty()

    def set_volume(self, volume):
        self.volume = volume

    def _apply_difficulty(self):
        presets = {
            'easy':   {'enemy_speed': 150, 'spawn_interval': 1200, 'max_enemies': 10},
            'normal': {'enemy_speed': 250, 'spawn_interval': 800, 'max_enemies': 20},
            'hard':   {'enemy_speed': 350, 'spawn_interval': 400, 'max_enemies': 35},
        }
        preset = presets[self.difficulty]
        self.enemy_speed = preset['enemy_speed']
        self.spawn_interval = preset['spawn_interval']
        self.max_enemies = preset['max_enemies']