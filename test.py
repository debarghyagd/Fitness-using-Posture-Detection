import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Get the screen dimensions
screen_info = pygame.display.Info()
width, height = screen_info.current_w, screen_info.current_h

# Create a full-screen window
screen = pygame.display.set_mode((1280, 800))

# Load the two frames
frame1 = pygame.image.load('./frame/1.png').convert()
frame2 = pygame.image.load('./frame/2.png').convert()

frames = [frame1, frame2]
current_frame = 0

clock = pygame.time.Clock()


class Image_Button:
    def __init__(self, screen, path, x_pos, y_pos, enabled):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.enabled = enabled
        self.image = pygame.image.load(path).convert()
        self.image_rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))
        screen = screen

    def draw(self):
        screen.blit(self.image, self.image_rect)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        return left_click and self.image_rect.collidepoint(mouse_pos)


class Text_Button:
    def __init__(self, screen, text, x_pos, y_pos, enabled, font_size=18):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        screen = screen
        self.enabled = enabled
        self.font_size = font_size

    def draw(self):
        clr1 = (0, 0, 0)  # text colour
        clr2 = (255, 255, 255)  # text background
        font = pygame.font.Font('Orbitron-Bold.ttf', self.font_size)
        text_render = font.render(self.text, True, clr1, clr2)
        self.textRect = text_render.get_rect()
        self.textRect.center = (self.x_pos, self.y_pos)
        screen.blit(text_render, self.textRect)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        return left_click and self.textRect.collidepoint(mouse_pos) and self.enabled


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Show the current frame
    screen.blit(frames[current_frame], (0, 0))
    
    obj1 = Image_Button(screen, './Images/YOGA.png', 1142, 644, True)
    obj1.draw()
    # if obj1.check_click():
    #     return 0

    obj2 = Image_Button(screen, './Images/WORKOUT.png', 10, 644, True)
    obj2.draw()
    # if obj2.check_click():
        # return 1

    obj3 = Text_Button(screen, 'FITRO', 640, 225, True, 96)
    obj3.draw()

    pygame.display.flip()

    # Delay to control the frame rate
    clock.tick(5)

    # Switch to the next frame
    current_frame = (current_frame + 1) % len(frames)
