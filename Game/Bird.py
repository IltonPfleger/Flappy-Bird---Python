from Utils import Rectangle, Color, Button, Text, Point, Window
import random

class Bird:
    gravity = 0.001
    strength = gravity*1000/3
    sprite = "Images/bird.png"

    def __init__(self):
        self.alive = True
        self.rectangle = Rectangle(Window.center[0]/5, Window.center[1], 40, 30)
        self.velocity = 0

    def fly(self):
        self.velocity = -Bird.strength

    def die(self):
        self.alive = False

    def update(self, click: bool):
        if click:
            self.fly()
        y = self.rectangle.y + self.velocity
        self.velocity += Bird.gravity
        self.rectangle.y = y
