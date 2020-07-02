######################################
# Import and initialize the librarys #
######################################
from pygame_objects import *


selection_screen = screen(
    name = 'selection',

    surfaceParameters = {
        'frame': coord(w=1024, h=768),
        'bgColour': None,
        'isAlpha': True
    }, 
    objectsParameters = {
        'background': {
            'type': 'object',
            'isAlpha': True,
            'frame': {
                'image': coord(w=1024, h=768)
            }
        },
        'bubble': {
            'type': 'button',
            'isAlpha': True,
            'frame': {
                'box': coord(x=261, y=243, w=689, h=59), 
                'image': coord(w=1024, h=768),
                'text': coord(x=281, y=248, w=646, h=49), 
            },
            'runclass': 'Bubble sort'
        },
        'insertion': {
            'type': 'button',
            'isAlpha': True,
            'frame': {
                'box': coord(x=261, y=300, w=689, h=59), 
                'image': coord(w=1024, h=768)
            },
            'runclass': 'Insertion sort'
        },
        'merge': {
            'type': 'button',
            'isAlpha': True,
            'frame': {
                'box': coord(x=261, y=358, w=689, h=59), 
                'image': coord(w=1024, h=768)
            },
            'runclass': 'Merge sort'
        },
        'quick': {
            'type': 'button',
            'isAlpha': True,
            'frame': {
                'box': coord(x=261, y=415, w=689, h=59), 
                'image': coord(w=1024, h=768)
            },
            'runclass': 'Quick sort'
        },
        'radix': {
            'type': 'button',
            'isAlpha': True,
            'frame': {
                'box': coord(x=261, y=473, w=689, h=59), 
                'image': coord(w=1024, h=768)
            },
            'runclass': 'Radix sort'
        },
        'bogo': {
            'type': 'button',
            'isAlpha': True,
            'frame': {
                'box': coord(x=261, y=531, w=689, h=59), 
                'image': coord(w=1024, h=768)
            },
            'runclass': 'Bogo sort'
        },
        'arrow': {
            'type': 'button',
            'frame': {
                'box': coord(x=897, y=160, w=53, h=53), 
                'image': coord(x=892, y=160, w=53, h=53), 
            },
            'runclass': '__back__'
        }
    }
)


selection_screen.surface.load()

class selection:

    def run(screen, itemName):
        # Display home screen
        selection_screen.surface.display(withLoad=False)
        screen.objects[itemName].display(directToScreen=True)

        while True:
            # Get check for interaction with screen
            action_result = selection_screen.event.action(directToScreen=True)

            # No action
            if action_result == None: continue

            # When program is set to close
            elif action_result.didAction('quit'): return '__quit__'

            elif action_result.didAction('click'):
                if not action_result.click.isItem('arrow'):
                    screen.objects[itemName].data.setText(text=action_result.click.outcome, withDisplay=False)
                return '__back__'