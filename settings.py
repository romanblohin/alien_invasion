class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 640
        self.screen_height = 480
        self.bg_color = (230, 230, 230)
        # Настройки корабля 
        self.ship_speed = 5
        # Параметры снаряда 
        self.bullet_speed = 1
        self.bullet_width = 3 
        self.bullet_height = 15 
        self.bullets_allowed = 3
        self.bullet_color = (60, 60, 60)