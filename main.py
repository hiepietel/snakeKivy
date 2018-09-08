from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import *
from kivy.clock import Clock
from random import randint
from kivy.config import Config
from kivy.properties import StringProperty

windowHeight = 720
windowWidth = 1280


class SnakeStart(BoxLayout):
    def __init__(self, **kwargs):
        super(SnakeStart, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modfiers):
        if keycode[1] == "spacebar":
            gameOn = True


class SnakeEnd(BoxLayout):
    pass


class SnakeWindow(BoxLayout):
    #strScore = StringProperty()
    score = -1
    pos_x = 200
    pos_y = 200
    cur_x = 1
    cur_y = 0
    speed = 40
    snakeSize = appleSize = (40, 40)
    apple_x = -100
    apple_y = -100
    apple_offset = 40
    points_x = []
    points_y = []
    rectangles = []

    def __init__(self, **kwargs):
        super(SnakeWindow, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.intro()
        self.score = 0

    def intro(self):
        #gameOn = True
        self.pos_x = windowWidth / 2
        self.pos_y = windowHeight / 2
        self.points_x.insert(0, self.pos_x)
        self.points_y.insert(0, self.pos_y)
        with self.canvas:
            #Color(.8, .4, 0)
            self.a = Rectangle(source = 'apple.png', pos=(self.apple_x, self.apple_y), size=self.appleSize)
            Color(.6, .5, .4)
            i = 1
            while i < 50:
                self.rectangles.append(Rectangle(source='body.png', pos=(-100, -100), size=self.snakeSize))
                i += 1
            #Color(.6, .6, .6)
            self.rectangles.insert(0, Rectangle( source = 'head1.png', pos=(self.pos_x, self.pos_y), size=self.snakeSize))
            #self.rectangles[0].angle = 45
            #self.rectangles[0].pos=(self.pos_x, self.pos_y)

            #self.rectangles[0].color(.4, .7, .9)

        self.randApple()
        self.lbl = Label(text="score: 0",
                         color=(.6, .7, .8, 1),
                         font_size='20sp',
                         halign="left",
                         valign = "top",
                         size_hint=(.1, .1)) #pos=(windowWidth-100, windowHeight/2))
        #print(lbl.pos)
        #self.lbl.pos = (windowWidth-100, windowHeight - self.lbl.height -20)
        self.add_widget(self.lbl)
        print(self.lbl.pos)

    def randApple(self):
        self.apple_x = randint(0 + self.apple_offset/40, (windowWidth-2*self.apple_offset)/40)*40
        self.apple_y = randint(0 + self.apple_offset/40, (windowHeight-self.apple_offset)/40)*40
        i = 0
        while i < self.score:
            while self.points_x[i] == self.apple_x and self.points_y[i] == self.apple_y:
                self.apple_x = randint(0 + self.apple_offset / 40, (windowWidth - 2 * self.apple_offset) / 40) * 40
                self.apple_y = randint(0 + self.apple_offset / 40, (windowHeight - self.apple_offset) / 40) * 40
            i += 1
        print(str(self.apple_x)+" "+str(self.apple_y))
        self.a.pos = (self.apple_x, self.apple_y)

    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modfiers):

        if keycode[1] == "left":
            self.cur_x = -1
            self.cur_y = 0
        if keycode[1] == "right":
            self.cur_x = 1
            self.cur_y = 0
        if keycode[1] == "down":
            self.cur_y = -1
            self.cur_x = 0
        if keycode[1] == "up":
            self.cur_y = 1
            self.cur_x = 0

    def update(self, dt):
        self.pos_x += self.speed * self.cur_x
        self.pos_y += self.speed * self.cur_y
        if self.cur_x == -1:
            self.rectangles[0].source = "headleft.png"
        elif self.cur_x == 1:
            self.rectangles[0].source = "headright.png"
        elif self.cur_y == 1:
            self.rectangles[0].source = "headup.png"
        elif self.cur_y == -1:
            self.rectangles[0].source = "headdown.png"

        if self.points_x[0] == self.apple_x and self.points_y[0] == self.apple_y:
            print("got it")
            self.randApple()
            self.score += 1
            self.lbl.text = "score: "+str(self.score)
        else:
            self.points_x.pop()
            self.points_y.pop()
        self.points_x.insert(0, self.pos_x)
        self.points_y.insert(0, self.pos_y)
        i = 1
        #self.rectangles[0].Rotate.angle = (45)
        if self.pos_x < 0 or self.pos_x > windowWidth or self.pos_y < 0 or self.pos_y > windowHeight:
            print("game over")
            #gameOn = False
        #sprawdzenie czy waz nie je siebie
        i = 1
        while i < self.score+1:
            if self.points_x[i] == self.pos_x and self.points_y[i] == self.pos_y:
                print("game over")
                #gameOn = False
            i += 1
        i = 0
        while i < self.score+1:
            self.rectangles[i].pos = (self.points_x[i], self.points_y[i])
            i += 1


class SnakeGameApp(App):
    def build(self):
        #box = BoxLayout()
        Config.set("graphics", "borderless", 1)
        Config.set('graphics', 'width', windowWidth)
        Config.set('graphics', 'height', windowHeight)
        Config.write()
        #print(Window().height)
        snakeWindow = SnakeWindow()
        Clock.schedule_interval(snakeWindow.update, 1.0/6.0)
        snakeEnd = SnakeEnd()
        return snakeWindow


if __name__ == "__main__":
    SnakeGameApp().run()
