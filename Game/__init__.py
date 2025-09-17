import random
from Utils import Rectangle, Color, Button, Text, Point, Window
from .Pipe import Pipe, HardPipe

class Game():
    def __init__(self):
        self.paused = False
        self.buttons = []
        self.buttons.append(Button(Rectangle(Window.width - 50, 0, 50, 50), Color(0, 0, 0), self.pause))
        self.score = 0
        self.texts = [Text("Score: 0", 0, 0)]
        self.velocity = 0.5
        self.gravity = 0.005
        self.pipes = [Pipe(self.velocity)]

    def pause(self):
        self.paused = not self.paused

    def update(self, mouse : Point, click):
        for button in self.buttons:
            if(button.rectangle.collidepoint(mouse) and click):
                button.action()

        if(self.paused):
            return None

        if(self.pipes[-1].rectangles[0].x < Window.center[0]):
            self.pipes.append(HardPipe(self.velocity) if random.random() > 0.5 else Pipe(self.velocity))
        if(self.pipes[0].rectangles[0].x + Pipe.width < 0):
            self.score += 1
            self.texts[0].text = "Score: " + str(self.score)
            del self.pipes[0]
        for pipe in self.pipes:
            pipe.move()


