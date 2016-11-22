#!/usr/bin/env python

'''
ZAC is an acronym for 'Zack and Cody'. 
This game is based on a mind training game 
shown at "The Suite Life of Zack & Cody" movie.

Started coding at 10/21/2012 and finished at 11/22/2012

My son owns the tv remote control now, so Disney Channel it is.
'''

#-------------------Imports-------------------
import pygame
from pygame.locals import *
from os import path
from random import randint, shuffle
from io import open
from sys import platform

#-------------------Constants-------------------
SIZE = (800,440)
VERSION = '0.1'
DATA_FOLDER = 'zac_data'
MAIN_COLOR = 'PaleGoldenrod'
_FONT = 'TimesNewRoman'

#-------------------Global functions-------------------
def load_sound(name):
    return pygame.mixer.Sound(path.join(DATA_FOLDER, name))

def display_some_text(text,size,image,orientation,color='black'):
    font = pygame.font.SysFont(_FONT, size)
    t = font.render(text, 1, Color(color))
    trect = t.get_rect()
    if orientation == 'left':
        trect.left = 0
        trect.centery = image.get_rect().height/2
    elif orientation == 'center':
        trect.centerx = image.get_rect().width/2
        trect.centery = image.get_rect().height/2
    elif orientation == 'right':
        trect.right = image.get_rect().width
        trect.centery = image.get_rect().height/2
    else:
        trect.center = orientation
    image.blit(t, trect)

def lines(opened_file):
    line_list = []
    counter = 0
    while 1:
        line = opened_file[counter]
        line_list.append(line)
        counter += 1
        if line == '\n':
            break
    return line_list

#-------------------Classes-------------------
class simple_button:
    def __init__(self,x,y,title,background):
        self.background = background
        self.image = pygame.Surface([100,40])
        self.image.fill(Color(MAIN_COLOR))
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        if background.mustlock():background.lock()
        # Draw the border
        pygame.draw.rect(self.image,Color("black"),(0,0,self.rect.width,self.rect.height),1)
        # Draw some shadow lines
        pygame.draw.line(background,Color("black"),(x+1,y+self.rect.height),(x+self.rect.width-1,y+self.rect.height)) #horizontal
        pygame.draw.line(background,Color("black"),(x+self.rect.width,y+1),(x+self.rect.width,y+self.rect.height)) #vertical
        if background.get_locked():background.unlock()
        # Display some text
        display_some_text(title,23,self.image,'center')
        self.background.blit(self.image,self.rect)
        self.status = 0
        self.is_dirty = 0
    def press(self):
        self.rect.inflate_ip(-2,-2)
        self.status = 1
        self.is_dirty = 1
    def unpress(self):
        self.rect.inflate_ip(2,2)
        self.status = 0
        self.is_dirty = 1
    def is_focused(self,x,y):
        return self.rect.collidepoint(x,y)
    def update(self):
        if self.is_dirty:
            self.background.blit(self.image,self.rect)
            self.is_dirty = 0

class score_board:
    def __init__(self,background,score):
        x = 675
        y = 156
        self.background = background
        self.image = pygame.Surface((90,40)).convert()
        self.image.fill(Color(MAIN_COLOR))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y+40)
        self.score = score
        display_some_text(str(self.score),25,self.image,'right')
        self.background.blit(self.image,self.rect)
        self.image2 = pygame.Surface((100,40)).convert()
        self.image2.fill(Color(MAIN_COLOR))
        self.rect2 = self.image2.get_rect()
        self.rect2.topleft = (x,y)
        display_some_text('SCORE',25,self.image2,'center')
        self.background.blit(self.image2,self.rect2)
        self.background.lock()
        pygame.draw.rect(self.background, Color('BLACK'), (x-1,y-1,102,82),1)
        self.background.unlock()
        self.is_dirty = 0
    def update(self):
        self.image.fill(Color(MAIN_COLOR))
        display_some_text(str(self.score),25,self.image,'right')
        self.background.blit(self.image,self.rect)

class guess_board:
    def __init__(self,background,guessing_times):
        x = 675
        y = 264
        self.background = background
        self.image = pygame.Surface((90,40)).convert()
        self.image.fill(Color(MAIN_COLOR))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y+40)
        self.guessing_times = guessing_times
        display_some_text(str(self.guessing_times),25,self.image,'right')
        self.background.blit(self.image,self.rect)
        self.image2 = pygame.Surface((100,40)).convert()
        self.image2.fill(Color(MAIN_COLOR))
        self.rect2 = self.image2.get_rect()
        self.rect2.topleft = (x,y)
        display_some_text('GUESS',25,self.image2,'center')
        self.background.blit(self.image2,self.rect2)
        self.background.lock()
        pygame.draw.rect(self.background, Color('BLACK'), (x-1,y-1,102,82),1)
        self.background.unlock()
        self.is_dirty = 0
    def update(self):
        self.image.fill(Color(MAIN_COLOR))
        display_some_text(str(self.guessing_times),25,self.image,'right')
        self.background.blit(self.image,self.rect)

class time_board:
    def __init__(self,background):
        self.background = background
        self.image = pygame.Surface((100,100)).convert()
        self.image.fill(Color(MAIN_COLOR))
        self.rect = self.image.get_rect()
        self.rect.topleft = (675,28)
        self.guessing_time = 5
        self.timer = -1
    def write_on_board(self,reverse_timer):
        self.image.fill(Color(MAIN_COLOR))
        display_some_text(str(reverse_timer),105,self.image,'center')
        self.background.blit(self.image,self.rect)

class main_board:
    def __init__(self,background):
        self.background = background
        self.image = pygame.Surface((630,260)).convert()
        self.image.fill(Color(MAIN_COLOR))
        self.rect = self.image.get_rect()
        self.rect.topleft = (20,20)
    def write_on_board(self,text,color):
        self.image.fill(Color(MAIN_COLOR))
        if text in ['TURQUOISE','CHOCOLATE','CHARTREUSE','OLIVEDRAB']:
            size = 95
        else:
            size = 130
        display_some_text(text,size,self.image,'center',color)
        self.background.blit(self.image,self.rect)

class gameplay:
    def __init__(self,background,guessing_times,score,mode,colors,level,text,color,returns_from_about):
        self.background = background
        self.background.fill(Color(MAIN_COLOR))
        self.good_sound = load_sound('crowd yeah.ogg')
        self.bad_sound = load_sound('dissapointed.ogg')
        self.b1 = guess_board(background,guessing_times)
        self.b2 = simple_button(675,372,'ABOUT',background)
        self.b3 = score_board(background,score)
        self.b4 = time_board(background)
        self.b5 = main_board(background)
        self.guessing_text = ''
        self.mode = mode
        self.colors = colors
        self.level = level
        self.text = text
        self.color = color
        self.returns_from_about = returns_from_about
        self.game_has_ended = 0
        self.set_mode(background,mode)

    def set_mode(self,background,mode):
        self.color_holder_list = []
        x = 20
        if self.returns_from_about:
            for color in self.colors:
                self.color_holder_list.append(color_holder(background,color,(x,310)))
                x += 130
            self.b5.write_on_board(self.text,self.color)
            self.returns_from_about = 0
        else:
            self.colors1 = ['RED','ORANGE','YELLOW','GREEN','BLUE']
            self.colors2 = ['PINK','MAGENTA','SALMON','GOLD','BROWN','CYAN','GREY','TURQUOISE'\
                            ,'CHOCOLATE','TOMATO','VIOLET','CORAL','CHARTREUSE'\
                            ,'OLIVEDRAB','RED','ORANGE','YELLOW','GREEN','BLUE']
            if mode == 'normal':
                self.colors = self.colors1
            elif mode == 'hard':
                _colors2 = []
                for s in range(5):
                    shuffle(self.colors2)
                    _colors2.append(self.colors2.pop())
                self.colors = _colors2
            for color in self.colors:
                self.color_holder_list.append(color_holder(background,color,(x,310)))
                x += 130
            self.text, self.color = self._shuffle(self.colors)
            self.b5.write_on_board(self.text,self.color)
            self.mode = mode

    def _shuffle(self,colors):
        _colors = colors[:]
        shuffle(_colors)
        text = _colors.pop()
        shuffle(_colors)
        color = _colors.pop()
        return text,color

    def update(self):
        if self.guessing_text == self.text:
            self.good_sound.play()
            self.b3.score += 1
            if self.b3.score == 100:
                self.game_has_ended = 1
            self.b1.guessing_times += 1
        else:
            self.bad_sound.play()
            if self.b3.score >= 1:
                self.b3.score -= 1
            self.b1.guessing_times = 0

        if self.b1.guessing_times == 10:
            self.colors = []
            self.b1.guessing_times = 0
            self.level += 1
            if not self.game_has_ended:
                self.set_mode(self.background,'hard')
        elif self.b3.score == 0 and self.level >= 1 and not self.mode == 'normal':
            self.colors = []
            self.level = 0
            self.set_mode(self.background,'normal')

        if self.game_has_ended:
            return -1
        else:
            self.b3.update()
            self.b1.update()
            a1 = self.text
            a2 = self.text
            b1 = self.color
            b2 = self.color
            while a1 == a2 and b1 == b2:
                a2, b2 = self._shuffle(self.colors)
            self.text = a2
            self.color = b2
            self.b5.write_on_board(self.text,self.color)
            self.guessing_text = ''

class color_holder:
    def __init__(self,background,color,topleft):
        self.background = background
        self.color = color
        self.image = pygame.Surface((110,110)).convert()
        self.image.fill(Color(color))
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
        self.background.blit(self.image,self.rect)
    def update(self,color):
        self.image.fill(Color(color))
        self.background.blit(self.image,self.rect)
    def is_focused(self,x,y):
        return self.rect.collidepoint(x,y)

#-------------------Game functions-------------------
def start(background):
    musicfile = path.join(DATA_FOLDER,'SPFAIRY.mid')
    pygame.mixer.music.load(musicfile)
    pygame.mixer.music.play(-1)

    background.fill(Color(MAIN_COLOR))
    display_some_text('Z A C',200,background,(400,150))
    display_some_text('K   E   E   P         Y   O   U   R         C   O   I   N',18,background,(400,250))
    b = simple_button(350,380,'START',background)

    running = 1
    var = 0
    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = 0
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                if b.is_focused(event.pos[0],event.pos[1]):
                    b.press()
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                if b.status:
                    b.unpress()
                    var = 1
                    running = 0
        b.update()
        pygame.display.update()

    del b
    return var

def play(background,guessing_times,score,mode,colors,level,text,color,returns_from_about,music):
    if music == 'Plum':
        pass
    elif music == 'Death':
        pygame.mixer.music.stop()
        musicfile = path.join(DATA_FOLDER,'SPFAIRY.mid')
        pygame.mixer.music.load(musicfile)
        pygame.mixer.music.play(-1)

    a = gameplay(background,guessing_times,score,mode,colors,level,text,color,returns_from_about)
    running = 1
    var = 0

    CLOCK = pygame.time.Clock()
    time = 0
    timer = -1

    while running:
        time += CLOCK.tick()
        _time = time / 1000
        if _time > a.b4.guessing_time - 1:
            time = 0
            _time = 0
            a.update()
        if timer != _time:
            timer = _time
            reverse_timer = a.b4.guessing_time - timer
            a.b4.write_on_board(reverse_timer)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = 0
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                if a.b2.is_focused(event.pos[0],event.pos[1]):
                    a.b2.press()
                else:
                    for x in a.color_holder_list:
                        if x.is_focused(event.pos[0],event.pos[1]):
                            a.guessing_text = x.color
                            time = 0
                            _time = 0
                            if a.update() == -1:
                                var = -1
                                running = 0
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                if a.b2.status:
                    a.b2.unpress()
                    var = 1
                    running = 0
            a.b2.update()
        pygame.display.update()

    _guess_ = a.b1.guessing_times
    _score_ = a.b3.score
    _mode_ = a.mode
    _colors_ = a.colors
    _level_ = a.level
    _text_ = a.text
    _color_ = a.color
    _returns_from_about_ = a.returns_from_about

    for x in a.color_holder_list:
        del x
    del a.b1,a.b2,a.b3,a.b4,a.b5,time,timer,_time,reverse_timer
    return [var,_guess_,_score_,_mode_,_colors_,_level_,_text_,_color_,_returns_from_about_]

def about(background):
    pygame.mixer.music.stop()
    musicfile = path.join(DATA_FOLDER,'dance of death.mid')
    pygame.mixer.music.load(musicfile)
    pygame.mixer.music.play(-1)

    background.fill(Color(MAIN_COLOR))
    b1 = simple_button(250,380,'NEXT',background)
    b2 = simple_button(450,380,'OK',background)

    in_file = open(path.join(DATA_FOLDER,'info.txt'))
    opened_file = in_file.readlines()
    in_file.close()
    _len = 0
    _len_ = len(opened_file)
    line_list = lines(opened_file[_len:])
    l = len(line_list)
    _len += l
    y = (10 - l)/2 * 50
    for line in line_list:
        display_some_text(line.strip('\n'),25,background,(400,y))
        y += 50

    running = 1
    var = 0

    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = 0
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                if b1.is_focused(event.pos[0],event.pos[1]):
                    b1.press()
                elif b2.is_focused(event.pos[0],event.pos[1]):
                    b2.press()
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                if b1.status:
                    b1.unpress()
                    background.fill(Color(MAIN_COLOR),(10,10,780,360))
                    if _len >= _len_:
                        _len = 0
                    line_list = lines(opened_file[_len:])
                    l = len(line_list)
                    _len += l
                    y = (10 - l)/2 * 50
                    for line in line_list:
                        display_some_text(line.strip('\n'),25,background,(400,y))
                        y += 50
                elif b2.status:
                    b2.unpress()
                    var = 1
                    running = 0
        b1.update()
        b2.update()
        pygame.display.update()

    del b1,b2,opened_file,_len,_len_,line_list,l,y,running
    pygame.mixer.music.stop()
    return var

def end_game(background,level):
    background.fill(Color(MAIN_COLOR))
    b1 = simple_button(250,380,'PLAY',background)
    b2 = simple_button(450,380,'EXIT',background)

    if level == 0:
        a = 'FINISHED'
        b = 'YOUR SCORE REACHED 100 BUT YOU DID NOT CHANGE ANY LEVEL...'
    else:
        if level == 1:
            s = ''
        else:
            s = 'S'
    a = 'WELL DONE !'
    b = 'YOUR SCORE REACHED 100 & YOU CHANGED '+str(level)+' LEVEL'+s
    c = 'PLAY AGAIN?'
    display_some_text(a,70,background,(400,150))
    display_some_text(b,23,background,(400,250))
    display_some_text(c,23,background,(400,300))

    running = 1
    var = 0

    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = 0
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                if b1.is_focused(event.pos[0],event.pos[1]):
                    b1.press()
                elif b2.is_focused(event.pos[0],event.pos[1]):
                    b2.press()
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                if b1.status:
                    b1.unpress()
                    var = 1
                    running = 0
                elif b2.status:
                    b2.unpress()
                    running = 0
        b1.update()
        b2.update()
        pygame.display.update()

    del b1,b2,running
    return var

def main():
    pygame.init()
    background = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("ZAC v" + VERSION)

    kwargs = {'guessing_times':0,'score':0,'mode':'normal','colors':[],'level':0,'text':'','color':'','returns_from_about':0,'music':'Plum'}
    a = start(background)
    while a:
        b = play(background, **kwargs)
        while b[0] == 1:
            c = about(background)
            if not c:
                a = 0
                break
            kwargs = {'guessing_times':b[1],'score':b[2],'mode':b[3],'colors':b[4],'level':b[5],'text':b[6],'color':b[7],'returns_from_about':1,'music':'Death'}
            break
        while b[0] == -1:
            d = end_game(background,b[5])
            if not d:
                a = 0
                break
            kwargs = {'guessing_times':0,'score':0,'mode':'normal','colors':[],'level':0,'text':'','color':'','returns_from_about':0,'music':'Plum'}
            break
        while not b[0]:
            a = 0
            break

    pygame.quit()

if __name__ == '__main__': main()
