######################################
# Import and initialize the librarys #
#####################################
from pygame_objects import *
#from algorithm.bubblesort import bubblesort


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
                suffix = ' swaps per sec',
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
            'data': text(
                text = '104.20',
                editable = False,
                suffix = ' sec',
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


class sort:

    def bubblesort(speed:int):
        count = 1
        while True:
            array = sort_screen.objects.sortbox.data

            # Compare each pair
            didSwap = False
            for index in range(array.bars - count):
                array.barslist[index].state('selected')
                array.barslist[index+1].state('selected')
                sort_screen.objects.sortbox.display()

                select_time = time.time()
                while time.time() - select_time < speed/2: action_result = sort_screen.event.action()

                if array.barslist[index+1].number < array.barslist[index].number:
                    array.swap(index, index+1, speed)
                    didSwap = True

                array.barslist[index].state()

                select_time = time.time()
                while time.time() - select_time < speed/2: action_result = sort_screen.event.action()

            count += 1
            
            array.barslist[index+1].state()

            # If all pairs are sorted
            if not didSwap: break

        sort_screen.objects.sortbox.data.completed()


    def run(screen, sortType:str, bars:int, speed:float):
        # Set data from parent
        sort_screen.objects.sortbox.data.bars = int(bars)

        # Display home screen
        sort_screen.surface.display()

        sort.bubblesort(speed)

        while True:
            # sort_screen.objects.sortbox.data.move(39, 0)

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