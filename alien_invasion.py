import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        #self.settings.screen_width = self.screen.get_rect().width
        #self.settings.screen_height = self.screen.get_rect().height
        
        pygame.display.set_caption("Alien Invasion")

        # Создание экземпляров для хранения статистики
        # и панели результатов.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self._create_buttons()

    def _create_buttons(self):
        '''Создаем кнопку Play и кнопки для выбора уровня сложности'''
        # Создание кнопки Play.
        screen_rect = self.screen.get_rect()
        green_color = (0, 255, 0)
        white_color = (255, 255, 255)
        black_color = (0, 0, 0)
        self.play_button = Button(self, "Play", 'center', 'center',200, 50, green_color, black_color, 48)
        
        self.middle_button = Button(self, "Middle", self.play_button.rect.x + 25, 
            self.play_button.rect.bottom + 25, 150, 50, green_color, black_color, 32)
        self.easy_button = Button(self, "Easy", self.middle_button.rect.x - 175, self.middle_button.rect.y,
             150, 50, white_color, black_color, 32)
        self.hard_button = Button(self, "Hard", self.middle_button.rect.right + 25, self.middle_button.rect.y,
             150, 50, white_color, black_color, 32)

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Уменьшение ships_left и обновление панели счета
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            
            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
            
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            
            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Проверяет, добрались ли пришельцы до нижнего края экрана."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Происходит то же, что при столкновении с кораблем.
                self._ship_hit()
                break

    def _create_fleet(self): 
        """Создание флота вторжения."""
        # Создание пришельца и вычисление количества пришельцев в ряду 
        # Интервал между соседними пришельцами равен ширине пришельца.

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size 
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        """Определяет количество рядов, помещающихся на экране."""
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - 
            (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Создание флота вторжения. 
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number): 
        """Создание пришельца и размещение его в ряду."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number 
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self): 
        """Реагирует на достижение пришельцем края экрана."""
        for alien in self.aliens.sprites(): 
            if alien.check_edges():
                self._change_fleet_direction() 
                break

    def _change_fleet_direction(self): 
        """Опускает весь флот и меняет направление флота."""
        for alien in self.aliens.sprites(): 
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def run_game(self):
        """Start the main loop for the game."""
        while True:

            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()                        
            
            self._update_screen()
            

    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды."""
        # Обновление позиций снарядов.
        self.bullets.update()

        # Удаление снарядов, вышедших за край экрана. 
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0: 
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Обработка коллизий снарядов с пришельцами."""
        # Удаление снарядов и пришельцев, участвующих в коллизиях.

        # Проверка попаданий в пришельцев.
        # При обнаружении попадания удалить снаряд и пришельца.
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Уничтожение существующих снарядов и создание нового флота.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Увеличение уровня.
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self): 
        """Обновляет позиции всех пришельцев во флоте."""
        self._check_fleet_edges() 
        self.aliens.update()

        # Проверка коллизий "пришелец — корабль".
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Проверить, добрались ли пришельцы до нижнего края экрана.
        self._check_aliens_bottom()

    def _check_events(self):
        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)                
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_button_clicked(mouse_pos)

    def _check_button_clicked(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки Play."""

        green_color = (0, 255, 0)
        white_color = (255, 255, 255)

        play_button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        middle_button_clicked = self.middle_button.rect.collidepoint(mouse_pos)
        easy_button_clicked = self.easy_button.rect.collidepoint(mouse_pos)
        hard_button_clicked = self.hard_button.rect.collidepoint(mouse_pos)

        if not self.stats.game_active:
            
            if play_button_clicked:
                # Сброс игровых настроек.
                self.start_game()
            elif middle_button_clicked:
                self.settings.level = 'middle'
                self.settings.initialize_dynamic_settings()
                self.middle_button.button_color = green_color
                self.middle_button._prep_msg('Middle')
                self.hard_button.button_color = white_color
                self.hard_button._prep_msg('Hard')
                self.easy_button.button_color = white_color
                self.easy_button._prep_msg('Easy')
            elif easy_button_clicked:
                self.settings.level = 'easy'
                self.settings.initialize_dynamic_settings()
                self.easy_button.button_color = green_color
                self.easy_button._prep_msg('Easy')
                self.middle_button.button_color = white_color
                self.middle_button._prep_msg('Middle')
                self.hard_button.button_color = white_color
                self.hard_button._prep_msg('Hard')
            elif hard_button_clicked:
                self.settings.level = 'hard'
                self.settings.initialize_dynamic_settings()
                self.hard_button.button_color = green_color
                self.hard_button._prep_msg('Hard')
                self.easy_button.button_color = white_color
                self.easy_button._prep_msg('Easy')
                self.middle_button.button_color = white_color
                self.middle_button._prep_msg('Middle')
                
    def start_game(self):
        # Сброс игровой статистики.
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        # Очистка списков пришельцев и снарядов.
        self.aliens.empty()
        self.bullets.empty()

        # Создание нового флота и размещение корабля в центре.
        self._create_fleet()
        self.ship.center_ship()

        # Указатель мыши скрывается.
        pygame.mouse.set_visible(False)
                
    def _check_keydown_events(self, event): 
        """Реагирует на нажатие клавиш."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT: 
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_p and not self.stats.game_active:
            # Сброс игровых настроек.
            self.start_game()
        elif event.key == pygame.K_SPACE: 
            self._fire_bullet()

    def _check_keyup_events(self, event): 
        """Реагирует на отпускание клавиш."""
        if event.key == pygame.K_RIGHT: 
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT: 
            self.ship.moving_left = False

    def _fire_bullet(self): 
        """Создание нового снаряда и включение его в группу bullets."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self) 
            self.bullets.add(new_bullet)

    def _update_screen(self):
        # При каждом проходе цикла перерисовывается экран. 
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites(): 
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        # Вывод информации о счете.
        self.sb.show_score()

        # Кнопка Play отображается в том случае, если игра неактивна.
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.middle_button.draw_button()
            self.easy_button.draw_button()
            self.hard_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()