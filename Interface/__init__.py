from Utils import Rectangle, Color, Button, Text, TextButton, ImageButton, Window, Point, Image
from Game import Game, Bird
from Game.Cenário.Pipe import Pipe, HardPipe
from Game.Cenário.Ground import Ground
import pygame

class Interface():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Window.width, Window.height))
        self.mouse = None
        self.click = False
        self.key = False
        self.sprites = {}
        self.load(Image(Ground.sprite, Rectangle(0, 0, Window.width, Ground.height)))
        self.game = Game()
        self.load(Image(Bird.sprite, self.game.birds[0].rectangle))
        self.load(Image("Images/pause.png", self.game.pauseButton.rectangle))
        self.load(Image("Images/play.png", self.game.playButton.rectangle))

    def load(self, image : Image):
        self.sprites[image.dir] = pygame.transform.scale(pygame.image.load(image.dir), (image.rectangle.w, image.rectangle.h))

    def image(self, image, content = None, rectangle = None):
        if(content != None):
            self.screen.blit(content, rectangle)
        else:
            self.screen.blit(self.sprites[image.dir], image.rectangle.tuple)

    def rectangle(self, r : Rectangle, c : Color):
        pygame.draw.rect(self.screen, c.tuple, r.tuple)

    def button(self, b : Button):
        self.rectangle(b.rectangle, b.color)

    def textButton(self, b: Button):
        self.rectangle(b.rectangle, b.color)
        self.text(b.text)
        
    def imageButton(self, b : Button):
        self.image(b.image)


    def text(self, t : Text):
        font = pygame.font.SysFont(None, t.size)
        surface = font.render(t.text, True, t.color.tuple)
        rectangle = None
        if t.align == "topleft":
            rectangle = surface.get_rect(topleft=(t.x, t.y))
        else:
            rectangle = surface.get_rect(center=(t.x, t.y))
        self.screen.blit(surface, rectangle)

    def bird(self, bird : Bird):
        angled = pygame.transform.rotate(self.sprites[Bird.sprite], bird.velocity * 10)
        rectangle = angled.get_rect(center=pygame.Rect(bird.rectangle.tuple).center)
        self.image(Image("", rectangle), angled, rectangle)

    def pipe(self, pipe : Pipe):
        for rectangle in pipe.rectangles:
            self.rectangle(rectangle, pipe.color)

    def loop(self):
        while True:
            self.click = False
            self.key = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.click = True
                if event.type == pygame.KEYDOWN:
                    self.key = event.key

            pygame.display.flip()
            self.mouse = pygame.mouse.get_pos()
            self.screen.fill(Window.background.tuple)

            if not self.game.update(Point(self.mouse[0], self.mouse[1]), self.click, self.key):
                exit()

            for obj in self.game.renderables():
                if isinstance(obj, Bird):
                    self.bird(obj)
                if isinstance(obj, Pipe) or isinstance(obj, HardPipe):
                    self.pipe(obj)
                if isinstance(obj, Button):
                    self.button(obj)
                if isinstance(obj, Text):
                    self.text(obj)
                if isinstance(obj, Image):
                    self.image(obj)
                if isinstance(obj, TextButton):
                    self.textButton(obj)
                if isinstance(obj, ImageButton):
                    self.imageButton(obj)


    def run(self):
        self.loop()


