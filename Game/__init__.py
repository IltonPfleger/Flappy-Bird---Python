from Utils import Rectangle, Color, Button, TextButton, ImageButton, Image, Text, Point, Window
from .Cenário.Pipe import Pipe, HardPipe
from .Cenário.Ground import Ground
from .Bird import Bird, Birds
import random
import os


class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Game(metaclass=SingletonMeta):
    def __init__(self):
        self.state = "start"
        self.score = 0
        self.max_score = self.load_max_score()
        self.ground = Ground()
        self.pipes = [Pipe()]
        self.AI = True
        self.birds = Birds(self.AI)

        self.init_buttons()

    def init_buttons(self):
        center_x, center_y = Window.center

        self.playButton = ImageButton(
                Rectangle(center_x - 50, center_y - 50, 100, 100),
                Window.background,
                self.pause,
                Image("Images/play.png", Rectangle(center_x - 50, center_y - 50, 100, 100))
                )
        self.pauseButton = ImageButton(
                Rectangle(Window.width - 20, 0, 20, 20),
                Window.background,
                self.pause,
                Image("Images/pause.png", Rectangle(Window.width - 20, 0, 20, 20))
                )
        self.restartButton = TextButton(
                Rectangle(center_x - 50, center_y - 50, 100, 50),
                Color(0, 0, 0),
                self.restart,
                Text("Reiniciar", Color(255, 255, 255))
                )
        self.exitButton = TextButton(
                Rectangle(center_x - 50, center_y + 100, 100, 50),
                Color(0, 0, 0),
                self.exit,
                Text("Sair", Color(255, 255, 255))
                )
        self.killAllButton = TextButton(
                Rectangle(center_x - 70, center_y + 160, 140, 50),
                Color(0, 0, 0),
                self.killall,
                Text("Matar Todos", Color(255, 255, 255))
                )

    # -----------------------------
    # Score Methods
    # -----------------------------
    def load_max_score(self):
        if os.path.exists("max_score.txt"):
            with open("max_score.txt", "r") as file:
                try:
                    return int(file.read())
                except ValueError:
                    return 0
        return 0

    def save_max_score(self):
        with open("max_score.txt", "w") as file:
            file.write(str(self.max_score))

    # -----------------------------
    # Game Control Methods
    # -----------------------------
    def restart(self):
        self.state = "running"
        self.score = 0
        self.pipes = [Pipe()]
        self.birds.regenerate()

    def killall(self):
        self.birds.killall(self.score)
        self.gameover()

    def exit(self):
        self.save_max_score()
        self.state = "exit"

    def pause(self):
        if self.state in ["running", "start"]:
            self.state = "paused" if self.state == "running" else "running"

    def gameover(self):
        self.max_score = max(self.max_score, self.score)
        self.save_max_score()
        self.state = "gameover"
        self.restart()

    # -----------------------------
    # UI Methods
    # -----------------------------
    def buttons(self):
        mapping = {
                "start": [self.playButton],
                "running": [self.pauseButton],
                "paused": [self.playButton, self.exitButton, self.killAllButton],
                "gameover": [self.restartButton, self.exitButton]
                }
        return mapping.get(self.state, [])

    def renderables(self):
        renderables = []

        if self.state == "gameover":
            renderables.append(Text(f"Pontuação: {int(self.score)}", Color(0, 0, 0), Text.BIG, Window.width/2, 100, "center"))
        elif self.state == "running":
            renderables.extend(self.birds)
            renderables.extend(self.pipes)
            renderables.append(self.ground.image)
            renderables.append(Text(f"Pontuação: {self.score}", Color(0, 0, 0)))
            renderables.append(Text(f"Vivos: {len(self.birds)}", Color(0, 0, 0), Text.NORMAL, 0, 20))
        elif self.state == "start":
            renderables.append(Text(f"Pontuação Máxima: {self.max_score}", Color(0, 0, 0), Text.BIG, Window.width/2, 200, "center"))

        renderables.extend(self.buttons())
        return renderables

    # -----------------------------
    # Update Game Logic
    # -----------------------------
    def update(self, mouse: Point, click, key):
        for button in self.buttons():
            if button.rectangle.collidepoint(mouse) and click:
                button.action()

        if self.state in ["paused", "gameover"]:
            return True

        # Add new pipes
        if self.pipes[-1].rectangles[0].x < Window.center[0] - Pipe.width:
            self.pipes.append(HardPipe() if random.random() > 0.5 else Pipe())

        # Remove passed pipes and increment score
        if self.pipes[0].rectangles[0].x + Pipe.width < 0:
            self.score += 1
            self.pipes.pop(0)

        # Update pipes
        for pipe in self.pipes:
            pipe.update()

        # Determine the current pipe
        current_pipe = next((p for p in self.pipes if p.rectangles[0].x + p.width > Bird.x), None)

        # Update birds
        for bird in self.birds:
            bird.update(current_pipe.rectangles[0].x, current_pipe.seed, click or key)
            if self.check_collision(bird):
                self.birds.kill(bird, self.score)

        if self.state == "exit":
            return False

        if len(self.birds) == 0:
            self.gameover()

        return True

    def check_collision(self, bird):
        if bird.rectangle.y < 0 or bird.rectangle.y + bird.rectangle.h > Window.height - Ground.height:
            return True
        for rectangle in self.pipes[0].rectangles:
            if rectangle.colliderect(bird.rectangle):
                return True
        return False

