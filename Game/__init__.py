from Utils import Rectangle, Color, Button, TextButton, ImageButton, Image, Text, Point, Window
from .Cenário.Pipe import Pipe, HardPipe
from .Cenário.Ground import Ground
from .Bird import Bird, Birds
import random
import os


class Game():
    def __init__(self):
        self.state = "start"
        self.score = self.load_max_score()
        self.max_score = 0
        self.ground = Ground()
        self.pipes = [Pipe()]
        self.AI = True
        self.birds = Birds(self.AI)
        self.died = []

        #Buttons
        playButtonRectangle  = Rectangle(Window.center[0] - 50, Window.center[1] - 50, 100, 100)
        self.playButton = ImageButton(playButtonRectangle, Window.background, self.pause, Image("Images/play.png", playButtonRectangle))
        pauseButtonRectangle = Rectangle(Window.width - 20, 0, 20, 20)
        self.pauseButton = ImageButton(pauseButtonRectangle, Window.background, self.pause, Image("Images/pause.png", pauseButtonRectangle))
        self.restartButton = TextButton(Rectangle(Window.center[0] - 50, Window.center[1] - 50, 100, 50), Color(0, 0, 0), self.restart, Text("Reiniciar", Color(255,255,255)))
        self.exitButton = TextButton(Rectangle(Window.center[0] - 50, Window.center[1] + 100, 100, 50), Color(0, 0, 0), self.exit, Text("Sair", Color(255,255,255)))
        self.killAllButton = TextButton(Rectangle(Window.center[0] - 70, Window.center[1] + 160, 140, 50), Color(0, 0, 0), self.killall, Text("Matar Todos", Color(255,255,255)))

    def load_max_score(self):
        if os.path.exists("max_score.txt"):
            with open("max_score.txt", "r") as file:
                return int(file.read())
        return 0

    def save_max_score(self):
        with open("max_score.txt", "w") as file:
            file.write(str(self.max_score))

    def restart(self):
        self.state = "running"
        self.score = 0
        self.pipes = [Pipe()]
        self.birds.regenerate()

    def killall(self):
        self.birds.killall(self.score)
        self.gameover()

    def buttons(self):
        if(self.state == "gameover"):
            return [self.restartButton, self.exitButton]
        elif self.state == "running":
            return [self.pauseButton]
        elif self.state == "paused":
            return [self.playButton, self.exitButton, self.killAllButton]
        elif self.state == "start":
            return [self.playButton]

    def exit(self):
        self.save_max_score()
        self.state = "exit"

    def gameover(self):
        if self.score > self.max_score:
            self.max_score = self.score
            self.save_max_score()
        self.state = "gameover"
        self.restart()

    def pause(self):
        if self.state == "running":
            self.state = "paused"
        elif self.state == "paused":
            self.state = "running"
        elif self.state == "start":
            self.state = "running"

    def renderables(self):
        renderables = []

        if self.state == "gameover":
            score = Text(f"Pontuação: {int(self.score)}", Color(0,0,0), Text.BIG, Window.width/2, 100, "center")
            renderables.append(score)
        elif self.state == "running":
            renderables.extend(self.birds)
            renderables.extend(self.pipes)
            renderables.append(self.ground.image)
            score = Text(f"Pontuação: {self.score}", Color(0,0,0))
            alive = Text(f"Vivos: {len(self.birds)}", Color(0,0,0), Text.NORMAL, 0, 20)
            renderables.append(score)
            renderables.append(alive)
        elif self.state == "paused":
            pass
        elif self.state == "start":
            score = Text(f"Pontuação Máxima: {int(self.score)}", Color(0,0,0), Text.BIG, Window.width/2, 200, "center")
            renderables.append(score)
        renderables.extend(self.buttons())
        return renderables

    def update(self, mouse : Point, click, key):
        for button in self.buttons():
            if(button.rectangle.collidepoint(mouse) and click):
                button.action()

        if self.state in ["paused","gameover"]:
            return True

        #self.score += 0.001
        if(self.pipes[-1].rectangles[0].x < Window.center[0] - Pipe.width):
            self.pipes.append(HardPipe() if random.random() > 0.5 else Pipe())
        if(self.pipes[0].rectangles[0].x + Pipe.width < 0):
            self.score += 1
            del self.pipes[0]
        for pipe in self.pipes:
            pipe.update()

        current = None
        for pipe in self.pipes:
            if(pipe.rectangles[0].x + pipe.width > Bird.x):
                current = pipe
                break

        for bird in self.birds:
            bird.update(current.rectangles[0].x, current.seed, click or key)
            die = False
            for rectangle in self.pipes[0].rectangles:
                if rectangle.colliderect(bird.rectangle):
                    die = True
                    break
                if bird.rectangle.y < 0 or bird.rectangle.y + bird.rectangle.h > Window.height - Ground.height:
                    die = True

            if die:
                self.birds.kill(bird, self.score)

        if self.state == "exit":
            return False

        if len(self.birds) == 0:
            self.gameover()

        return True
