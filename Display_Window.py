from sys import exit
import pygame
from Loading import Window
from Yoga_Pose_Choice import Choose_Yoga
from Curl_Counter import Count


class Display:
    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 800), FULLSCREEN)
        self.clock = pygame.time.Clock()

    def driver(self):
        pygame.init()
        while True:
            obj = Window(self.screen)
            k = obj.driver()
            if k == 0:
                # obj2 = Choose_Yoga(self.screen)
                # obj2.driver()
                pass
            else:
                obj2 = Count()
                obj2.driver()


obj = Display()
obj.driver()
