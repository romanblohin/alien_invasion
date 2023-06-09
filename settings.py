class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 640
        self.screen_height = 480
        self.bg_color = (230, 230, 230)
        # Настройки корабля 
        self.ship_limit = 2
        # Параметры снаряда 
        self.bullet_width = 3 
        self.bullet_height = 15 
        self.bullets_allowed = 10
        self.bullet_color = (60, 60, 60)
        # Настройки пришельцев 
        self.fleet_drop_speed = 10 
        
        # Темп ускорения игры
        self.speedup_scale = 1.1

        # Темп роста стоимости пришельцев
        self.score_scale = 1.5

        # Уровень игры
        self.level = 'middle'

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Инициализирует настройки, изменяющиеся в ходе игры."""
        if self.level == 'easy':
            self.ship_speed = 1.0
            self.bullet_speed = 2.0
            self.alien_speed = 0.5
        elif self.level == 'middle':
            self.ship_speed = 1.5
            self.bullet_speed = 3.0
            self.alien_speed = 1.0
        elif self.level == 'hard':
            self.ship_speed = 2.0
            self.bullet_speed = 4.0
            self.alien_speed = 1.5

        # fleet_direction = 1 обозначает движение вправо; а -1 - влево.
        self.fleet_direction = 1

        # Подсчет очков
        self.alien_points = 50

    def increase_speed(self):
        """Увеличивает настройки скорости и стоимость пришельцев."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)