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
    def __init__(self, frame:Frame, text:str = '', prefix:str = '', suffix:str = '',
    format_:TextFormat = None, validation:TextValidate = None, editable:bool = True):
        self._frame = frame
        self._text = text
        self._prefix = prefix
        self._suffix = suffix
        self._format = TextFormat() if format_ is None else format_
        self._validation = TextValidate() if validation is None else validation
        self._editable = editable

    def setUp(self, surface):
        self.surface = surface
        self.renderText()

    def renderText(self):
        # Generate surface for text
        self.textSurface = pygame.surface.Surface(self._frame.size(), pygame.SRCALPHA)
        # Get text with prefix and suffix
        text = self.getText()
        
        # Set \n as a new line when display
        line_text = text.split('\n')

        # Warp the text
        if self._format.warpText == None:
            warpped_text = line_text
        
        else:
            warpped_text = []
            for line in line_text:
                warpped_text += textwrap.wrap(line, width=self._format.warpText)
        
        # generate text to surface
        h = 0
        for line in warpped_text:
            # Size of text line
            text_w, text_h = self._format.font.size(line)

            # Render the text line and store to text surface
            rendered_text = self._format.font.render(line, True, self._format.colour)

            # Render line based on alignment
            if self._format.align == 'left': self.textSurface.blit(rendered_text, (0, h))
            elif self._format.align == 'right': self.textSurface.blit(rendered_text, (self._frame.w - text_w, h))
            elif self._format.align == 'center': self.textSurface.blit(rendered_text, (int((self._frame.w - text_w)/2), h))

            self.textHeight = h
            # Set hight of next line
            h += text_h * self._format.lineSpacing
        
        self.textHeight += text_h
    
    def loadWithState(self):
        if self._format.pos == 'top': self.surface.getScreen().blit(self.textSurface, self._frame.coord())
        elif self._format.pos == 'bottom': self.surface.getScreen().blit(self.textSurface, (self._frame.x, self._frame.y + (self._frame.h - self.textHeight)))
        elif self._format.pos == 'center': self.surface.getScreen().blit(self.textSurface, (self._frame.x, self._frame.y + int((self._frame.h - self.textHeight)/2)))
        else: Logger.get().error('Unknown text postion type: "{}"'.format(self._format.pos))

    def validateChar(self, char, inAscii = True):
        # Ensure that character is allowed for that textfield
        if self._validation.inAscii and not inAscii: char = ord(char)
        elif not self._validation.inAscii and inAscii: char = chr(char)

        return char in self._validation.charsAllowed

    def validateText(self):
        # Check for regex matching
        valid = self._validation
        regexTexts = valid.regex.findall(self._text)
        Logger.get().debug('[{}] Regex matching result of {}'.format(self.item.name, regexTexts))

        # Full match
        if len(regexTexts) == 1 and regexTexts[0] == self._text: 
            if callable(valid.customMethod): return valid.customMethod(self._text)
            return True

        # Invalid based on regex
        else:
            return False
    
    def setText(self, text:str = None, prefix:str = None, suffix:str = None):
        if text != None: self._text = str(text)
        if prefix != None: self._prefix = str(prefix)
        if suffix != None: self._suffix = str(suffix)

        self.renderText()
        self.surface.display()
    
    def getText(self):
        # Combine prefix, text and suffix
        try:
            if self.surface.isState('selected') and self._editable: return self._prefix+self._text+'_'+self._suffix
            else: return self._prefix+self._text+self._suffix
        
        # Error, usually due to prefix, text or suffix not being str
        except:
            Logger.get().error('Error getting text for {}'.format(self.name), exc_info=True)
            return None

    def getFrame(self):
        return self._frame

    def getFormat(self):
        return self._format

    def isEditable(self):
        return self._editable