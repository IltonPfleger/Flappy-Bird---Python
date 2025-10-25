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

    def colliderect(self, rect):
        return (
                self.x < rect.x + rect.w and
                self.x + self.w > rect.x and
                self.y < rect.y + rect.h and
                self.y + self.h > rect.y
                )

class Color():
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    @property
    def tuple(self):
        return (self.r, self.g, self.b)

class Image:
    def __init__(self, dir : str, rectangle : Rectangle):
        self.dir = dir
        self.rectangle = rectangle

class Text:
    SMALL=15
    NORMAL=30
    BIG=60

    def __init__(self, text : str, color : Color, size = NORMAL, x = 0, y = 0, align = "topleft"):
        self.x = x
        self.y = y
        self.size = size
        self.align = align
        self.text = text
        self.color = color

class Button:
    def __init__(self, rectangle : Rectangle, color : Color, action):
        self.action = action
        self.rectangle = rectangle
        self.color = color

    def action(self):
        self.action()

class TextButton(Button):
    def __init__(self, rectangle : Rectangle, colorbg : Color, action, text : Text):
        super().__init__(rectangle, colorbg, action)
        self.text = text
        text.align = "center"
        self.text.x = rectangle.x + rectangle.w/2
        self.text.y = rectangle.y + rectangle.h/2

class Window:
    width = 480
    height = 720
    center = (width/2, height/2)
    background = Color(255, 255, 100)
