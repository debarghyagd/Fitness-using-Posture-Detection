import pygame
import random
from sys import exit
from Button import Image_Button, Text_Button


class Window:

    def __init__(self, screen):
        self.screen = screen  # pygame.display.set_mode((800, 480))
        self.clock = pygame.time.Clock()

        self.open_eye = pygame.image.load('./Images/open.png').convert()
        self.left_eye = pygame.image.load('./Images/left-eye.png').convert()
        self.right_eye = pygame.image.load('./Images/right-eye.png').convert()
        self.left_mid_eye = pygame.image.load(
            './Images/left-mid-eye.png').convert()
        self.right_mid_eye = pygame.image.load(
            './Images/right-mid-eye.png').convert()
        self.close_eye = pygame.image.load('./Images/close.png').convert()
        self.partial_close = pygame.image.load(
            './Images/partial-close.png').convert()

        self.frame = 1

    def middle(self):  # 1
        if self.frame > 0 and self.frame <= 20:
            if self.frame == 20:
                self.frame = 0
            return self.open_eye

    def middle_left_shift(self):  # 2
        if self.frame > 0 and self.frame <= 10:
            return self.open_eye
        elif self.frame > 10 and self.frame <= 20:
            return self.left_mid_eye
        else:
            if self.frame == 30:
                self.frame = 0
            return self.left_eye

    def left_middle_shift(self):  # 3
        if self.frame > 0 and self.frame <= 10:
            return self.left_eye
        elif self.frame > 10 and self.frame <= 20:
            return self.left_mid_eye
        else:
            if self.frame == 30:
                self.frame = 0
            return self.open_eye

    def middle_right_shift(self):  # 4
        if self.frame > 0 and self.frame <= 10:
            return self.open_eye
        elif self.frame > 10 and self.frame <= 20:
            return self.left_mid_eye
        else:
            if self.frame == 30:
                self.frame = 0
            return self.left_eye

    def right_middle_shift(self):  # 5
        if self.frame > 0 and self.frame <= 10:
            return self.right_eye
        elif self.frame > 10 and self.frame <= 20:
            return self.right_mid_eye
        else:
            if self.frame == 30:
                self.frame = 0
            return self.open_eye

    def close(self, choice):  # 6
        if self.frame > 0 and self.frame <= 10:
            return self.partial_close
        elif self.frame > 10 and self.frame <= 30:
            return self.close_eye
        elif self.frame > 30 and self.frame <= 40:
            return self.partial_close
        elif self.frame > 40 and self.frame <= 60:
            if self.frame == 60:
                self.frame = 0
            if choice == 2:
                return self.left_eye
            elif choice == 4:
                return self.right_eye
            else:
                return self.open_eye

    def choose(self, last):
        k = random.randint(1, 100)
        if last == 1:
            if k % 3 == 0:
                return 6
            elif k % 3 == 1:
                return 2
            else:
                return 4
        if last == 2:
            if k % 2 == 0:
                return 3
            else:
                return 6
        if last == 3 or last == 5:
            return 1
        if last == 4:
            if k % 2 == 0:
                return 5
            else:
                return 6

    def driver(self):
        work_list = []
        last_to_last = None
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            if self.frame == 1:
                if len(work_list) == 0:
                    work_list.append(1)
                elif len(work_list) > 1:
                    last_to_last = work_list.pop(0)
                else:
                    last = work_list.pop(0)
                    if last == 6:
                        work_list.append(self.choose(last_to_last))
                        if work_list[0] == 6:
                            last = last_to_last
                    else:
                        work_list.append(self.choose(last))
                    last_to_last = last

            image = None
            if work_list[0] == 1:
                image = self.middle()
            elif work_list[0] == 2:
                image = self.middle_left_shift()
            elif work_list[0] == 3:
                image = self.left_middle_shift()
            elif work_list[0] == 4:
                image = self.middle_right_shift()
            elif work_list[0] == 5:
                image = self.right_middle_shift()
            else:
                image = self.close(last_to_last)

            self.frame += 1

            self.screen.blit(image, (0, 0))

            obj1 = Image_Button(
                self.screen, './Images/YOGA.png', 635, 322, True)
            obj1.draw()
            if obj1.check_click():
                return 0

            obj2 = Image_Button(
                self.screen, './Images/WORKOUT.png', -10, 322, True)
            obj2.draw()
            if obj2.check_click():
                return 1

            obj3 = Text_Button(self.screen, 'FITRO', 400, 30, False, 28)
            obj3.draw()

            # self.screen.blit(self.yoga_logo_icon, (680, 402))
            pygame.display.update()
            # print(self.c0)
            self.clock.tick(60)
