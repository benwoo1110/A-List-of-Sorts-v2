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
                'text': coord(x=269, y=160, w=628, h=53)
            },
            'data': text(
                text = 'Merge sort',
                format = textFormat(
                    fontType=pg_ess.font.futura,
                    fontSize=38,
                    colour=pg_ess.colour.black
                )
            ),
            'runclass': 'type'
        },
        'info': {
            'type': 'button',
            'frame': {
                'box': coord(x=219, y=241, w=751, h=211), 
                'image': coord(x=219, y=241, w=751, h=211),
                'text': coord(x=249, y=260, w=696, h=170)
            },
            'data': text(
                text = '',
                format = textFormat(
                    fontType=pg_ess.font.futura,
                    fontSize=31,
                    colour=pg_ess.colour.black,
                    warpText=48
                )
            ),
            'runclass': 'info'
        },
        'speed': {
            'type': 'textfield',
            'frame': {
                'box': coord(x=265, y=480, w=704, h=70), 
                'image': coord(x=265, y=480, w=704, h=70),
                'text': coord(x=290, y=491, w=654, h=53)
            },
            'data': text(
                text = '100.0 swaps per sec',
                format = textFormat(
                    fontType=pg_ess.font.futura,
                    fontSize=38,
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
                'text': coord(x=422, y=586, w=522, h=53)
            },
            'data': text(
                text = '1000 bars',
                format = textFormat(
                    fontType=pg_ess.font.futura,
                    fontSize=38,
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


info_text = {
    'Bubble sort': 'Bubble sort, is one of the most simplest sorting algorithm that repeatedly steps through the list, compares adjacent pairs and swaps them if they are in the wrong order. ',
    'Insertion sort': 'Insertion sort is a simple sorting algorithm that builds the final sorted array (or list) one item at a time. It can be simply implemented and is also efficient for (quite) small data sets.',
    'Merge sort': 'Merge sort an efficient, comparison-based sorting algorithm. It’s a divide and conquer algorithm that was invented by John von Neumann in 1945.',
    'Quick sort': 'Quick sort is an O(n log n) efficient sorting algorithm, serving as a systematic method for placing the elements of a random access file or an array in order.',
    'Radix sort': 'Radix sort is a non-comparative integer sorting algorithm that sorts data with integer keys by grouping keys by individual digits which share the same significant position and value.',
    'Bogo sort': 'Bogo sort is a highly ineffective sorting algorithm based on the generate and test paradigm. The function successively generates permutations of its input until it finds one that is sorted.',
}


###############
# Home screen #
###############
class home:

    def run():
        # Display home screen
        home.setInfoText()
        home_screen.surface.display()

        while True:
            action_result = home_screen.event.action()

            if action_result == None: continue

            elif action_result.didAction('quit'): 
                return '__quit__'

            elif action_result.didAction('click'):
                if action_result.click.outcome == '__quit__':
                    return '__quit__'

    def setInfoText(display:bool = False):
        home_screen.objects.info.data.text = info_text[home_screen.objects.type.data.text]
        if display: home_screen.objects.info.display()
        else: home_screen.objects.info.load()


#############
# Main loop #
#############
if __name__ == "__main__":
    home.run()
    pg_ess.core.quit()