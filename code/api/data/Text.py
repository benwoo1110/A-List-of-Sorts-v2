import textwrap
import re
import pygame

from code.api.core.Frame import Frame
from code.api.utils.Logger import Logger


class TextFormat:
    pygame.font.init()

    customFontsAvailable = dict()
    defaultFont = None

    @staticmethod
    def addCustomFonts(customFontsAvailable:dict):
        TextFormat.customFontsAvailable.update(**customFontsAvailable)

    @staticmethod
    def getCustomFont(font:str):
        return TextFormat.customFontsAvailable.get(font)

    @staticmethod
    def setDefaultFont(font:str):
        TextFormat.defaultFont = font

    def __init__(self, fontType:str = None, fontSize:int = 36, colour:tuple = (0,0,0), 
    warpText:int = None, align:str = 'left', pos:str = 'top', lineSpacing:int = 1):
        self.fontType = TextFormat.defaultFont if fontType == None else fontType
        self.fontSize = fontSize
        self.colour = colour
        self.warpText = warpText
        self.align = align
        self.pos = pos
        self.lineSpacing = lineSpacing
        self.font = pygame.font.Font(self.fontType, self.fontSize)

    def modifyFont(self, fontSize:int = None, fontType:str = None):
        # set new font size and type (if any)
        if fontSize != None: self.fontSize = fontSize
        if fontType != None: self.fontType = fontType

        # Regen the font
        self.font = pygame.font.Font(self.fontType, self.fontSize)


class TextValidate:
    def __init__(self, charsAllowed:list = list(range(32,65)) + list(range(91,127)) + [8], 
    inAscii:bool = True, regex:str = '[\w\D.]+', defaultText:str = 'default', customMethod:any = None, invalidPrompt:str = None):
        self.charsAllowed = charsAllowed
        self.inAscii = inAscii
        self.regex = re.compile(regex)
        self.defaultText = defaultText
        self.customMethod = customMethod
        self.invalidPrompt = invalidPrompt

class Text:
    def __init__(self, frame:Frame, text:str = '', prefix:str = '', suffix:str = '', name=None, item=None,
    format:TextFormat = None, validation:TextValidate = None, editable:bool = True):
        self.name = name
        self.item = item
        self.frame = frame
        self.text = text
        self.prefix = prefix
        self.suffix = suffix
        self.format = TextFormat() if format == None else format
        self.validation = TextValidate() if validation == None else validation
        self.editable = editable

    def setUp(self, surface):
        self.surface = surface
        self.renderText()

    def validateChar(self, char, inAscii = True):
        # Ensure that character is alloweed for that textfield
        if self.validation.inAscii and not inAscii: char = ord(char)
        elif not self.validation.inAscii and inAscii: char = chr(char)

        return char in self.validation.charsAllowed

    def validateText(self):
        # Check for regex matching
        valid = self.validation
        regexTexts = valid.regex.findall(self.text)
        Logger.get().debug('[{}] Regex matching result of {}'.format(self.item.name, regexTexts))

        # Full match
        if len(regexTexts) == 1 and regexTexts[0] == self.text: 
            if callable(valid.customMethod): return valid.customMethod(self.text)
            return True

        # Invalid based on regex
        else:
            '''
            if self.validation.invalidPrompt != None:
                # Error sound
                sound.error.play()

                # Tell user is invalid
                Alert(
                    type='notify', 
                    title='Invalid Input',
                    content=self.validation.invalidPrompt
                ).do()
            '''

            return False

    def getText(self):
        # Combine prefix, text and suffix
        try:
            if self.surface.isState('selected') and self.editable: return self.prefix+self.text+'_'+self.suffix
            else: return self.prefix+self.text+self.suffix
        
        # Error, usually due to prefix, text or suffix not being str
        except:
            Logger.get().error('Error getting text for {}'.format(self.name), exc_info=True)
            return 'Error'

    def setText(self, text:str = None, prefix:str = None, suffix:str = None):
        if text != None: self.text = str(text)
        if prefix != None: self.prefix = str(prefix)
        if suffix != None: self.suffix = str(suffix)

        self.renderText()
        self.surface.display()

    def renderText(self):
        # Generate surface for text
        self.textSurface = pygame.surface.Surface(self.frame.size(), pygame.SRCALPHA)
        # Get text with prefix and suffix
        text = self.getText()
        
        # Set \n as a new line when display
        line_text = text.split('\n')

        # Warp the text
        if self.format.warpText == None:
            warpped_text = line_text
        
        else:
            warpped_text = []
            for line in line_text:
                warpped_text += textwrap.wrap(line, width=self.format.warpText)
        
        # generate text to surface
        h = 0
        for line in warpped_text:
            # Size of text line
            text_w, text_h = self.format.font.size(line)

            # Render the text line and store to text surface
            rendered_text = self.format.font.render(line, True, self.format.colour)

            # Render line based on alignment
            if self.format.align == 'left': self.textSurface.blit(rendered_text, (0, h))
            elif self.format.align == 'right': self.textSurface.blit(rendered_text, (self.frame.w - text_w, h))
            elif self.format.align == 'center': self.textSurface.blit(rendered_text, (int((self.frame.w - text_w)/2), h))

            self.textHeight = h
            # Set hight of next line
            h += text_h * self.format.lineSpacing
        
        self.textHeight += text_h
    
    def loadWithState(self):
        if self.format.pos == 'top': self.surface.getScreen().blit(self.textSurface, self.frame.coord())
        elif self.format.pos == 'bottom': self.surface.getScreen().blit(self.textSurface, (self.frame.x, self.frame.y + (self.frame.h - self.textHeight)))
        elif self.format.pos == 'center': self.surface.getScreen().blit(self.textSurface, (self.frame.x, self.frame.y + int((self.frame.h - self.textHeight)/2)))
        else: Logger.get().error('Unknown text postion type: "{}"'.format(self.format.pos))
