######################################
# Import and initialize the librarys #
######################################
import pygame
from config import config


##################
# Initialization #
##################
pygame.init()
window = pygame.display.set_mode(config.screen_res())


#####################
# Core parent class #
#####################
class coreFunc:
    def __setitem__(self, name, value): self.__dict__[name] = value
    def __setattr__(self, name, value): self.__dict__[name] = value
    def __getitem__(self, name): return self.__dict__[name]
    def __str__(self): return '{}'.format(self.__dict__)


######################
# Essentials Classes #
######################
class pg_ess:

    ##########################
    # Common defined colours #
    ##########################
    class font:
        '''fonts found in fonts folder'''
        futura = './fonts/Futura.ttc'


    ##########################
    # Common defined colours #
    ##########################
    class colour:
        '''Common colour types in RGB tuple form'''
        black = (0, 0, 0)
        white = (255, 255, 255)
        gray = (43, 43, 43)
        whiteish = (213, 213, 213)
        orange = (255, 143, 8)
        selected = (150, 150, 150)
        red = (255, 100, 78)
        green = (136, 250, 78)
    

    ##################
    # Core functions #
    ##################
    class core:
        @staticmethod
        def caption(caption:str = 'pygame time!'):
            '''Set window header title'''
            pygame.display.set_caption(caption)
        
        @staticmethod
        def update(tick:int = config.ticks):
            '''Draw display changes to screen'''
            pygame.display.flip()
            pygame.display.update()
            pygame.time.Clock().tick_busy_loop(tick)
        
        @staticmethod
        def buffer() -> bool:
            '''Loop through pygame events and check of quit and scrolling'''
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return '__quit__'

        @staticmethod
        def quit():
            '''Exit from program'''
            pygame.quit()
