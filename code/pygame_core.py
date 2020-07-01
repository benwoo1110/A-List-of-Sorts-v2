######################################
# Import and initialize the librarys #
######################################
import logging
import pygame
from config import config


##################
# Initialization #
##################
pygame.init()


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
        red = (255, 0, 0)
        gray = (43, 43, 43)
        whiteish = (213, 213, 213)
        orange = (255, 143, 8)
    

    ##################
    # Core functions #
    ##################
    class core:
        def setCaption(caption:str = 'pygame time!'):
            '''Set window header title'''
            pygame.display.set_caption(caption)
            logging.debug('window captions set to {}'.format(caption))

        def update(tick:int = config.ticks):
            '''Draw display changes to screen'''
            pygame.display.flip()
            pygame.display.update()
            pygame.time.Clock().tick(tick)

        def buffer() -> bool:
            '''Loop through pygame events and check of quit and scrolling'''
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return True

        def quit():
            '''Exit from program'''
            logging.info('Exiting program...')
            pygame.quit()
