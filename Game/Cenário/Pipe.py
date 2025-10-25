from Utils import Rectangle, Color, Window
import random

class Pipe():
    velocity = 0.17
    width = 90
    aperture = 150
    capstone_diff = 15
    capstone_width = width + 2*capstone_diff
    color = Color(0, 255, 0)

    class Enum:
        Top = 0
        Bottom = 1
        Capstone_Top = 2
        Capstone_Bottom = 3

    def __init__(self):
        self.seed = random.randint(self.aperture, Window.height - self.aperture)
        self.rectangles = [None] * 4
        self.rectangles[Pipe.Enum.Top] = Rectangle(Window.width, 0, self.width, self.seed - self.aperture)
        self.rectangles[Pipe.Enum.Bottom] = Rectangle(Window.width, self.seed + self.aperture, self.width, Window.height)
        self.rectangles[Pipe.Enum.Capstone_Top] = Rectangle(Window.width - self.capstone_diff, self.rectangles[0].h, self.capstone_width, self.capstone_diff)
        self.rectangles[Pipe.Enum.Capstone_Bottom] = Rectangle(Window.width - self.capstone_diff, self.rectangles[1].y, self.capstone_width, self.capstone_diff)
        self.hvelocity = Pipe.velocity

    def update(self):
        for rectangle in self.rectangles:
            rectangle.x -= self.hvelocity

class HardPipe(Pipe) :
    def __init__(self):
        super().__init__()
        self.vvelocity = (random.random() * 0.4 - 0.2)

    def update(self):
        super().update()
        self.rectangles[Pipe.Enum.Top].h += self.vvelocity
        self.rectangles[Pipe.Enum.Capstone_Top].y += self.vvelocity
        self.rectangles[Pipe.Enum.Bottom].y += self.vvelocity
        self.rectangles[Pipe.Enum.Capstone_Bottom].y += self.vvelocity

        if(self.rectangles[Pipe.Enum.Capstone_Bottom].y > Window.height or self.rectangles[Pipe.Enum.Capstone_Top].y < 0):
            self.vvelocity *= -1


