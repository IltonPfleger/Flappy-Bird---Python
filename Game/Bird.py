from Utils import Rectangle, Color, Button, Text, Point, Window, Definitions
import random

class Bird:
    strength = Definitions.gravity*1000/3
    sprite = "Images/bird.png"

    def __init__(self):
        self.alive = True
        self.rectangles = []
        self.rectangles.append(Rectangle(Window.center[0]/5, Window.center[1], 40, 30))
        #self.color = Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.velocity = 0

    def fly(self):
        self.velocity = -Bird.strength

    def die(self):
        self.alive = False

    def update(self, click: bool):
        if click:
            self.fly()
        for rectangle in self.rectangles:
            y = rectangle.y + self.velocity
            self.velocity += Definitions.gravity
            rectangle.y = y
