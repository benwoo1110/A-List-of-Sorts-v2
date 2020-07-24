######################################
# Import and initialize the librarys #
#####################################
from code.pygame_objects import *
from code.algorithm.bubblesort import bubblesort
from code.algorithm.insertionsort import insertionsort
from code.algorithm.bogosort import bogosort
from code.algorithm.mergesort import mergesort
from code.algorithm.quicksort import quicksort
from code.algorithm.radixsort import radixsort
from code.algorithm.selectionsort import selectionsort


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


sort_screen = screen(
    name = 'sort',
    surfaceParameters = {
        'frame': coord(w=1024, h=768)
    }, 
    objectsParameters = {
        'background': {
            'type': 'object',
            'frame': {
                'image': coord(w=1024, h=768)
            },
        },
        'sort_title': {
            'type': 'title',
            'frame': {
                'image': coord(w=1024, h=135)
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
        'moves': {
            'type': 'text',
            'frame': {
                'image': coord(x=436, y=677, w=112, h=40),
                'text': coord(x=436, y=677, w=112, h=40)
            },
            'data': moves(
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

    @staticmethod
    def run(screen, sortType:str, bars:int, speed:float):
        # Set data from parent
        if sort_screen.objects.sortbox.data.bars != int(bars): sort_screen.objects.sortbox.data.bars = int(bars)
        else: sort_screen.objects.sortbox.data.genBars()
        sort_screen.objects.speed.data.text = str(speed)
        sort_screen.objects.list_length.data.text = str(bars)

        # Display home screen
        sort_screen.objects.sort_title.switchState(sortType, display=False)
        sort_screen.surface.display()

        sort_result = runSort[sortType](sort_screen, speed)
        if sort_result != None: return sort_result

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