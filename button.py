import pygame.font
 
class Button:
 
    def __init__(self, ai_game, msg, button_x, button_y, button_weight, button_height, 
        button_color, text_color, text_size):
        """Initialize button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        
        # Set the dimensions and properties of the button.
        self.width, self.height = button_weight, button_height
        self.button_color = button_color
        self.text_color = text_color
        self.font = pygame.font.SysFont(None, text_size)
        
        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        
        if button_x == 'center':
            self.rect.center = self.screen_rect.center
        else:
            self.rect.x = button_x
            self.rect.y = button_y
        
        # The button message needs to be prepped only once.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color,
                self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button and then draw message.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)