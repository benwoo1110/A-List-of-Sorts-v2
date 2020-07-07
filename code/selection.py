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
                'box': coord(w=1024, h=768),
                'image': coord(w=1024, h=768)
            },
            'runclass': runclass(action='__back__')
        },
        'bubble': {
            'type': 'button',
            'isAlpha': True,
            'frame': {
                'box': coord(x=261, y=243, w=689, h=59), 
                'image': coord(w=1024, h=768),
                'text': coord(x=281, y=248, w=646, h=49), 
            },
            'runclass': runclass(action='Bubble sort')
        },
        'insertion': {
            'type': 'button',
            'isAlpha': True,
            'frame': {
                'box': coord(x=261, y=300, w=689, h=59), 
                'image': coord(w=1024, h=768)
            },
            'runclass': runclass(action='Insertion sort')
        },
        'merge': {
            'type': 'button',
            'isAlpha': True,
            'frame': {
                'box': coord(x=261, y=358, w=689, h=59), 
                'image': coord(w=1024, h=768)
            },
            'runclass': runclass(action='Merge sort')
        },
        'quick': {
            'type': 'button',
            'isAlpha': True,
            'frame': {
                'box': coord(x=261, y=415, w=689, h=59), 
                'image': coord(w=1024, h=768)
            },
            'runclass': runclass(action='Quick sort')
        },
        'radix': {
            'type': 'button',
            'isAlpha': True,
            'frame': {
                'box': coord(x=261, y=473, w=689, h=59), 
                'image': coord(w=1024, h=768)
            },
            'runclass': runclass(action='Radix sort')
        },
        'bogo': {
            'type': 'button',
            'isAlpha': True,
            'frame': {
                'box': coord(x=261, y=531, w=689, h=59), 
                'image': coord(w=1024, h=768)
            },
            'runclass': runclass(action='Bogo sort')
        },
    },
    keyboardParameters = {
        'back': {
            'keys': {27},
            'runclass': runclass(action='__back__')
        }
    }
)


# Load items to screen
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

            # Going back
            elif action_result.contains('outcome', '__back__'): return '__back__'

            elif action_result.didAction('click'):
                screen.objects[itemName].data.setText(text=action_result.click.outcome, withDisplay=False)
                return '__back__'