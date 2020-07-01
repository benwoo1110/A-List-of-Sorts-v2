######################################
# Import and initialize the librarys #
######################################
from pygame_objects import *


###########################
# Set homescreen elements #
###########################
home_screen = screen(
    name = 'home',

    surface_parameters = {
        'frame': coord(w=1024, h=768)
    },

    objects_parameters = {
        'background': {
            'type': 'object',
            'frame': coord(w=1024, h=768)
        },
        'type': {
            'type': 'textfield',
            'frame': coord(bx=240, by=149, w=729, h=70, ix=240, iy=149),
            'runclass': 'type'
        },
        'info': {
            'type': 'button',
            'frame': coord(bx=219, by=241, w=751, h=211, ix=219, iy=241),
            'runclass': 'info'
        },
        'speed': {
            'type': 'textfield',
            'frame': coord(bx=265, by=480, w=704, h=70, ix=265, iy=480),
            'runclass': 'speed'
        },
        'list_length': {
            'type': 'textfield',
            'frame': coord(bx=397, by=574, w=572, h=70, ix=397, iy=574),
            'runclass': 'list_length'
        },
        'run': {
            'type': 'button',
            'frame': coord(bx=775, by=671, w=194, h=70, ix=775, iy=671),
            'runclass': 'run'
        }
    }
)




class home:

    def run():
        # Display home screen
        home_screen.surface.display()

        while True:
            action_result = home_screen.event.action()

            if action_result != None:
                if action_result.didAction('quit'): 
                    return '__quit__'

                elif action_result.didAction('click'):
                    print(action_result.click)


if __name__ == "__main__":
    home.run()
    pg_ess.core.quit()