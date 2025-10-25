from Utils import Rectangle, Color, Button, TextButton, Text, Point, Window
from .Cenário.Pipe import Pipe, HardPipe
from .Cenário.Ground import Ground
from .Bird import Bird
import random

class Game():
    def __init__(self):
        self.state = "running"
        self.score = 0
        self.nbirds = 1
        self.ground = Ground()
        self.pipes = [Pipe()]
        self.birds = []
        self.died = []
        self.create_birds()

        #Labels
        self.scoreText = Text("Pontuação: 0", Color(0,0,0))

        #Buttons
        self.pauseButton = Button(Rectangle(Window.width - 50, 0, 50, 50), Color(0, 0, 0), self.pause)
        self.restartButton = TextButton(Rectangle(Window.center[0] - 50, Window.center[1] - 50, 100, 50), Color(0, 0, 0), self.restart, Text("Reiniciar", Color(255,255,255)))
        self.exitButton = TextButton(Rectangle(Window.center[0] - 50, Window.center[1] + 10, 100, 50), Color(0, 0, 0), self.exit, Text("Sair", Color(255,255,255)))

    def restart(self):
        self.__init__()

    def create_birds(self):
        for i in range(self.nbirds):
            self.birds.append(Bird())

    def buttons(self):
        if(self.state == "gameover"):
            return [self.restartButton, self.exitButton]
        elif self.state == "running":
            return [self.pauseButton]

    def exit(self):
        self.state = "exit"

    def gameover(self):
        self.state = "gameover"

    def pause(self):
        self.state = "paused"

    def renderables(self):
        renderables = []

        if(self.state == "gameover"):
            renderables.extend(self.buttons())
            score = self.scoreText
            score.size = Text.BIG
            score.x = Window.width/2
            score.y = 100
            score.align = "center"
            renderables.append(score)
            return renderables

        renderables.extend(self.birds)
        renderables.extend(self.pipes)
        renderables.extend(self.buttons())
        renderables.append(self.scoreText)
        renderables.append(self.ground.image)

        return renderables

    def update(self, mouse : Point, click, key):
        for button in self.buttons():
            if(button.rectangle.collidepoint(mouse) and click):
                button.action()

        if self.state in ["paused","gameover"]:
            return True

        if(self.pipes[-1].rectangles[0].x < Window.center[0] - Pipe.width):
            self.pipes.append(HardPipe() if random.random() > 0.5 else Pipe())
        if(self.pipes[0].rectangles[0].x + Pipe.width < 0):
            self.score += 1
            self.scoreText.text = "Pontuação: " + str(self.score)
            del self.pipes[0]
        for pipe in self.pipes:
            pipe.update()

        for bird in self.birds:
            if not bird.alive:
                continue
            bird.update(click or key)
            die = False
            for rectangle in self.pipes[0].rectangles:
                if rectangle.colliderect(bird.rectangle):
                    die = True
                    break
                if bird.rectangle.y + bird.rectangle.h > Window.height - Ground.height:
                    die = True
                if die:
                    break
            if die:
                self.birds.remove(bird)
                bird.die()
                self.died.append(bird)

        if self.state == "exit":
            return False
 
        if len(self.birds) == 0:
            self.gameover()

        return True
