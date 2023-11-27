from Utils import Rectangle, Color, Button, Text, Point, Window, Definitions
from .Cenário.Pipe import Pipe, HardPipe
from .Cenário.Ground import Ground
from .Bird import Bird
import random

class Game():
    def __init__(self):
        self.paused = False
        self.buttons = []
        self.buttons.append(Button(Rectangle(Window.width - 50, 0, 50, 50), Color(0, 0, 0), self.pause))
        self.score = 0
        self.texts = [Text("Score: 0", 0, 0)]
        self.nbirds = 1
        self.ground = Ground()
        self.pipes = [Pipe(Definitions.velocity)]
        self.birds = []
        self.died = []
        self.create_birds()

    def create_birds(self):
        for i in range(self.nbirds):
            self.birds.append(Bird())

    def pause(self):
        self.paused = not self.paused

    def update(self, mouse : Point, click):
        for button in self.buttons:
            if(button.rectangle.collidepoint(mouse) and click):
                button.action()

        if(self.paused):
            return None

        if(self.pipes[-1].rectangles[0].x < Window.center[0] - Pipe.width):
            self.pipes.append(HardPipe(Definitions.velocity) if random.random() > 0.5 else Pipe(Definitions.velocity))
        if(self.pipes[0].rectangles[0].x + Pipe.width < 0):
            self.score += 1
            self.texts[0].text = "Score: " + str(self.score)
            del self.pipes[0]
        for pipe in self.pipes:
            pipe.update()

        for bird in self.birds:
            if not bird.alive:
                continue
            bird.update(click)
            die = False
            for rectangle in self.pipes[0].rectangles:
                for _rectangle in bird.rectangles:
                    if rectangle.colliderect(_rectangle):
                        die = True
                        break
                    if _rectangle.y + _rectangle.h > self.ground.rectangles[0].y:
                        die = True
                if die:
                    break
            if die:
                self.birds.remove(bird)
                bird.die()
                self.died.append(bird)


        if len(self.birds) == 0:
            self.pause()
