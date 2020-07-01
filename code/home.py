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
            'frame': {
                'image': coord(w=1024, h=768)
            }
        },
        'type': {
            'type': 'textfield',
            'frame': {
                'box': coord(x=240, y=149, w=729, h=70), 
                'image': coord(x=240, y=149, w=729, h=70), 
                'text': coord(x=268, y=157, w=628, h=53)
            },
            'data': text(
                text = 'Insertion sort',
                format = textFormat(
                    fontType=pg_ess.font.futura,
                    fontSize=42,
                    colour=pg_ess.colour.black
                )
            ),
            'runclass': 'type'
        },
        'info': {
            'type': 'button',
            'frame': {
                'box': coord(x=219, y=241, w=751, h=211), 
                'image': coord(x=219, y=241, w=751, h=211)
            },
            'runclass': 'info'
        },
        'speed': {
            'type': 'textfield',
            'frame': {
                'box': coord(x=265, y=480, w=704, h=70), 
                'image': coord(x=265, y=480, w=704, h=70),
                'text': coord(x=290, y=488, w=654, h=53)
            },
            'data': text(
                text = '100.0 swaps per sec',
                format = textFormat(
                    fontType=pg_ess.font.futura,
                    fontSize=42,
                    colour=pg_ess.colour.black
                )
            ),
            'runclass': 'speed'
        },
        'list_length': {
            'type': 'textfield',
            'frame': {
                'box': coord(x=397, y=574, w=572, h=70), 
                'image': coord(x=397, y=574, w=572, h=70), 
                'text': coord(x=422, y=583, w=522, h=53)
            },
            'data': text(
                text = '1000 bars',
                format = textFormat(
                    fontType=pg_ess.font.futura,
                    fontSize=42,
                    colour=pg_ess.colour.black
                )
            ),
            'runclass': 'list_length'
        },
        'run': {
            'type': 'button',
            'frame': {
                'box': coord(x=775, y=671, w=194, h=70), 
                'image': coord(x=775, y=671, w=194, h=70)
            },
            'runclass': 'run'
        }
    }
)


###############
# Home screen #
###############
class home:

    def run():
        # Display home screen
        home_screen.surface.display()

        while True:
            action_result = home_screen.event.action()

            if action_result == None: continue

            elif action_result.didAction('quit'): 
                return '__quit__'

            elif action_result.didAction('click'):
                if action_result.click.outcome == '__quit__':
                    return '__quit__'


if __name__ == "__main__":
    home.run()
    pg_ess.core.quit()