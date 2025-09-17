class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def tuple(self):
        return (self.x, self.y)

class Rectangle():
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    @property
    def tuple(self):
        return (self.x, self.y, self.w, self.h)

    def collidepoint(self, point : Point):
        return self.x < point.x < self.x + self.w and self.y < point.y < self.y + self.h

class Color():
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    @property
    def tuple(self):
        return (self.r, self.g, self.b)

class Button:
    def __init__(self, rectangle : Rectangle, color : Color, action):
        self.action = action
        self.rectangle = rectangle
        self.color = color

    def action(self):
        self.action()

class Text:
    def __init__(self, text : str, x, y):
        self.x = x
        self.y = y
        self.text = text

class Window():
    width = 800
    height = 720
    dimensions = (width, height)
    center = (dimensions[0]/2, dimensions[1]/2)
    background = Color(255,255,100)
