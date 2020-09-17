######################################
# Import and initialize the librarys #
######################################
from code.pygame_objects import *
from code.textfield import textfield
from code.selection import selection
from code.sort import sort


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


###########################
# Set homescreen elements #
###########################
home_screen = screen(
    name = 'home',
    surfaceParameters = {
        'frame': coord(w=1024, h=768)
    },
    objectsParameters = {
        'background': {
            'type': 'object',
            'frame': {
                'image': coord(w=1024, h=768)
            }
        },
        'type': {
            'type': 'textfield',
            'isAlpha': True,
            'frame': {
                'box': coord(x=246, y=149, w=729, h=70), 
                'image': coord(x=246, y=149, w=729, h=70), 
                'text': coord(x=271, y=159, w=628, h=53)
            },
            'data': text(
                text = 'Bubble sort',
                #editable = False,
                format = textFormat(
                    fontType=pg_ess.font.futura,
                    fontSize=38,
                    colour=pg_ess.colour.black
                )
            ),
            'dataAddSelf': True,
            'runclass': runclass(
                action=textfield.run,
                parameters={'itemName': 'type'}
            )
        },
        'info': {
            'type': 'button',
            'frame': {
                'box': coord(x=225, y=242, w=751, h=211), 
                'image': coord(x=225, y=242, w=751, h=211),
                'text': coord(x=252, y=260, w=696, h=170)
            },
            'data': text(
                text = '',
                editable = False,
                format = textFormat(
                    fontType=pg_ess.font.futura,
                    fontSize=31,
                    colour=pg_ess.colour.black,
                    warpText=48
                )
            ),
            'dataAddSelf': True,
            'runclass': runclass(action='info')
        },
        'speed': {
            'type': 'textfield',
            'frame': {
                'box': coord(x=271, y=480, w=704, h=70), 
                'image': coord(x=271, y=480, w=704, h=70),
                'text': coord(x=296, y=490, w=654, h=53)
            },
            'data': text(
                text = '1.0',
                suffix = ' sec per move',
                format = textFormat(
                    fontType=pg_ess.font.futura,
                    fontSize=38,
                    colour=pg_ess.colour.black
                ),
                validation = textValidate(
                    charsAllowed=list(range(48, 58)) + [8, 46],
                    regex='\d{1,2}\.\d{1,3}|\d{1,2}',
                    defaultText='1.0'
                )
            ),
            'dataAddSelf': True,
            'runclass': runclass(
                action=textfield.run,
                parameters={'itemName': 'speed'}
            )
        },
        'list_length': {
            'type': 'textfield',
            'frame': {
                'box': coord(x=403, y=575, w=572, h=70), 
                'image': coord(x=403, y=575, w=572, h=70), 
                'text': coord(x=428, y=585, w=522, h=53)
            },
            'data': text(
                text = '10',
                suffix = ' bars',
                format = textFormat(
                    fontType=pg_ess.font.futura,
                    fontSize=38,
                    colour=pg_ess.colour.black
                ),
                validation = textValidate(
                    charsAllowed=list(range(48, 58)) + [8],
                    regex='^([1-9][0-9]{0,1}|[1-3][0-9]{2}|400)$',
                    defaultText='10'
                )
            ),
            'dataAddSelf': True,
            'runclass': runclass(
                action=textfield.run,
                parameters={'itemName': 'list_length'}
            )
        },
        'run': {
            'type': 'button',
            'frame': {
                'box': coord(x=781, y=671, w=194, h=70), 
                'image': coord(x=781, y=671, w=194, h=70)
            },
            'runclass': runclass(
                action=sort.run,
                parameters={'sortType': 'Bubble sort', 'bars': 10, 'speed': 1}
                )
            
        }
    }
)


##########################################
# Info about the different sorting types #
##########################################
info_text = {
    'Bubble sort': 'Bubble sort, is one of the most simplest sorting algorithm that repeatedly steps through the list, compares adjacent pairs and swaps them if they are in the wrong order. ',
    'Insertion sort': 'Insertion sort is a simple sorting algorithm that builds the final sorted array (or list) one item at a time. It can be simply implemented and is also efficient for (quite) small data sets.',
    'Merge sort': 'Merge sort an efficient, comparison-based sorting algorithm. It’s a divide and conquer algorithm that was invented by John von Neumann in 1945.',
    'Quick sort': 'Quick sort is an O(n log n) efficient sorting algorithm, serving as a systematic method for placing the elements of a random access file or an array in order.',
    'Radix sort': 'Radix sort is a non-comparative integer sorting algorithm that sorts data with integer keys by grouping keys by individual digits which share the same significant position and value.',
    'Bogo sort': 'Bogo sort is a highly ineffective sorting algorithm based on the generate and test paradigm. The function successively generates permutations of its input until it finds one that is sorted.',
    'Selection sort': 'Selection sort is a simple, in-place comparison-based algorithm. The list is divided into two parts, sorted part at the left end and unsorted part at the right end.',
}


###############
# Home screen #
###############
class home:

    @staticmethod
    def run():
        # Display home screen
        home.setInfoText()
        home_screen.surface.display()

        while True:
            # Get check for interaction with screen
            action_result = home_screen.event.action()

            # No action
            if action_result == None: continue
            # When program is set to close
            if action_result.contains('outcome','__quit__'): return '__quit__'
            # Load back screen
            if action_result.contains('outcome', '__back__'): home_screen.surface.display(withLoad=False)

            # When an object is clicked
            if action_result.didAction('click'): 
                # The sort type is changed               
                if action_result.click.isItem('type'): home.setInfoText()

                # When speed is changed
                if action_result.click.isItem('speed'): 
                    home_screen.objects.run.runclass.parameters['speed'] = float(home_screen.objects.speed.data.text)

                # When bar numbers is changed 
                if action_result.click.isItem('list_length'): 
                    home_screen.objects.run.runclass.parameters['bars'] = int(home_screen.objects.list_length.data.text)

    @staticmethod
    def setInfoText():
        # Set info to the corresponding sort type
        sort_type = home_screen.objects.type.data.text
        if sort_type in info_text.keys():
            home_screen.objects.info.data.setText(info_text[sort_type])

        # Set as run parameter
        home_screen.objects.run.runclass.parameters['sortType'] = sort_type