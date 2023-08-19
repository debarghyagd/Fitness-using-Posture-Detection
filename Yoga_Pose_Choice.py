import pygame
from Button import Text_Button
from Yoga_Pose_Correction import Yoga_Pose_Correction


class Choose_Yoga:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.pose_map = [
            'Boat Pose or Paripurna Navasana',
            'Bound Angle Pose or Baddha Konasana',
            'Bow Pose or Dhanurasana',
            'Bridge Pose or Setu Bandha Sarvangasana',
            'Camel Pose or Ustrasana',
            'Chair Pose or Utkatasana',
            'Child Pose or Balasana',
            'Cobra Pose or Bhujangasana',
            'Corpse Pose or Savasana',
            'Cow Pose or Marjaryasana',
            'Dolphin Plank Pose or Makara Adho Mukha Svanasana',
            'Dolphin Pose or Ardha Pincha Mayurasana',
            'Extended Revolved Side Angle Pose or Utthita Parsvakonasana Left-Hand',
            'Extended Revolved Side Angle Pose or Utthita Parsvakonasana Right-Hand',
            'Extended Revolved Triangle Pose or Utthita Trikonasana Left-Handed',
            'Extended Revolved Triangle Pose or Utthita Trikonasana Right-Handed',
            'Garland Pose or Malasana',
            'Half Moon Pose or Ardhachandrasana'
        ]

    def driver(self):
        display_surface = pygame.display.set_mode((800, 480))
        disp_array = self.pose_map[:12]
        ini = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            objects = []
            X = 400
            Y = 60
            display_surface.fill((24, 17, 41))
            c = ini
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and len(disp_array) != 12:
                disp_array = self.pose_map[:12]
                ini = 0
            if keys[pygame.K_DOWN] and len(disp_array) == 12:
                disp_array = self.pose_map[12:]
                ini = 12
            Text_Button(self.screen, "CHOOSE YOUR YOGA POSTURE",
                        X, Y-35, True, 28).draw()
            for i in disp_array:
                c += 1
                obj = Text_Button(self.screen, str(c)+"."+i, X, Y, True)
                Y += 36
                obj.draw()
                objects.append(obj)
                if obj.check_click():
                    state=Yoga_Pose_Correction().driver(i)
                    if state:
                        return

            pygame.display.update()
            # print(self.c0)
            self.clock.tick(60)
