######################################
# Import and initialize the librarys #
#####################################
from pygame_objects import *
from algorithm.bubblesort import bubblesort
from algorithm.insertionsort import insertionsort
from algorithm.selectionsort import selectionsort


sort_screen = screen(
    name = 'sort',
    surfaceParameters = {
        'frame': coord(w=1024, h=768)
    }, 
    objectsParameters = {
        'background': {
            'type': 'object',
            'frame': {
                'box': coord(w=1024, h=768),
                'image': coord(w=1024, h=768)
            },
        },
        'back': {
            'type': 'button',
            'frame': {
                'box': coord(x=71, y=41, w=112, h=61),
                'image': coord(x=71, y=41, w=112, h=61)
            },
            'runclass': runclass(action='go_back')
        },
        'info': {
            'type': 'button',
            'frame': {
                'box': coord(x=841, y=40, w=112, h=61),
                'image': coord(x=841, y=40, w=112, h=61),
            },
            'runclass': runclass(action='info')
        },
        'speed': {
            'type': 'text',
            'frame': {
                'image': coord(x=349, y=630, w=254, h=40),
                'text': coord(x=349, y=630, w=254, h=40)
            },
            'data': text(
                text = '10',
                editable = False,
                suffix = ' sec per move',
                format = textFormat(
                    fontType=pg_ess.font.futura,
                    fontSize=28,
                    colour=pg_ess.colour.black
                )
            ),
            'dataAddSelf': True,
        },
        'swaps': {
            'type': 'text',
            'frame': {
                'image': coord(x=436, y=677, w=112, h=40),
                'text': coord(x=436, y=677, w=112, h=40)
            },
            'data': text(
                text = '100',
                editable = False,
                format = textFormat(
                    fontType=pg_ess.font.futura,
                    fontSize=28,
                    colour=pg_ess.colour.black
                )
            ),
            'dataAddSelf': True,
        },
        'time_taken': {
            'type': 'text',
            'frame': {
                'image': coord(x=768, y=630, w=177, h=40),
                'text': coord(x=768, y=630, w=177, h=40)
            },
            'data': timer(
                format = textFormat(
                    fontType=pg_ess.font.futura,
                    fontSize=28,
                    colour=pg_ess.colour.black
                )
            ),
            'dataAddSelf': True,
        },
        'list_length': {
            'type': 'text',
            'frame': {
                'image': coord(x=759, y=677, w=112, h=186),
               'text': coord(x=759, y=677, w=112, h=186)
            },
            'data': text(
                text = '100',
                editable = False,
                suffix = ' bars',
                format = textFormat(
                    fontType=pg_ess.font.futura,
                    fontSize=28,
                    colour=pg_ess.colour.black
                )
            ),
            'dataAddSelf': True,
        },
        'sortbox': {
            'type': 'object',
            'frame': {
                'box': coord(x=52, y=145, w=922, h=430),
                'image': coord(x=52, y=145, w=922, h=430)
            },
            'data': sortbars(
                bars=10,
            ),
            'dataAddSelf': True,
        }
    }
)


runSort = {
    'Bubble sort': bubblesort.run,
    'Insertion sort': insertionsort.run,
    'Merge sort': insertionsort.run,
    'Quick sort': insertionsort.run,
    'Radix sort': insertionsort.run,
    'Bogo sort': selectionsort.run
}


class sort:

    def run(screen, sortType:str, bars:int, speed:float):
        # Set data from parent
        sort_screen.objects.sortbox.data.bars = int(bars)
        sort_screen.objects.speed.data.text = str(speed)
        sort_screen.objects.list_length.data.text = str(bars)

        # Display home screen
        sort_screen.surface.display()

        runSort[sortType](sort_screen, speed)

        while True:
            # Get check for interaction with screen
            action_result = sort_screen.event.action()

            # No action
            if action_result == None: continue

            # When program is set to close
            if action_result.contains('outcome','__quit__'): return '__quit__'

            # Going back
            if action_result.contains('outcome', 'go_back'): return '__back__' 

            # Load back screen
            if action_result.contains('outcome', '__back__'): sort_screen.surface.display(withLoad=False)