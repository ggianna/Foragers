# This was taken from http://www.pygame.org/wiki/Spritesheet?parent=CookBook
# This class handles sprite sheets
# This was taken from www.scriptefun.com/transcript-2-using
# sprite-sheets-and-drawing-the-background
# I've added some code to fail if the file wasn't found..
# Note: When calling images_at the rect is the format:
# (x, y, x + offset, y + offset)
 
import pygame
 
class Spritesheet(object):
    
    def __init__(self, filename,  tile_width = 32,  tile_height = 32):
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
            self.tile_width = tile_width
            self.tile_height = tile_height
            self._cache = {};
        except pygame.error, message:
            print 'Unable to load spritesheet image:', filename
            raise SystemExit, message
            
    # Load a specific image from a specific rectangle
    def image_at_col_row(self, col,  row, colorkey = None):
        try:
              return self._cache[(col,  row)]
        except KeyError:
            rect = pygame.Rect( col * self.tile_width, row * self.tile_height, 
              self.tile_width, self.tile_height )
            self._cache[(col,  row)] = self.image_at(rect,  colorkey)
            return self._cache[(col,  row)]
            
    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert().convert_alpha()
        # Fill with bg
        image.fill((0,128,0))
        # Add image
        image.blit(self.sheet, (0, 0), rect)
        
        # TODO: Check
        #if colorkey is not None:
            #if colorkey is -1:
                #colorkey = image.get_at((0,0))
            #image.set_colorkey(colorkey, pygame.RLEACCEL)
        #return image
        return image
        
    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates" 
        return [self.image_at(rect, colorkey) for rect in rects]
    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)
