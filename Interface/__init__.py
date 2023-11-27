from Utils import Rectangle, Color, Button, Text, Window, Point
from Game import Game, Bird
import pygame

class Interface():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(Window.dimensions)
        self.game = Game()
        self.mouse = None
        self.click = False
        self.font = pygame.font.SysFont(None, 30)
        self.sprites = {}
        self.load()

    def load(self):
        ground = self.game.ground
        bird = self.game.birds[0]
        self.sprites[bird.sprite] = pygame.transform.scale(pygame.image.load(bird.sprite), (bird.rectangles[0].w, bird.rectangles[0].h))
        self.sprites[ground.sprite] = pygame.transform.scale(pygame.image.load(ground.sprite), (ground.rectangles[0].w, ground.rectangles[0].h))

    def image(self, surface : pygame.surface.Surface, r : Rectangle):
        self.screen.blit(surface, r)

    def rectangle(self, r : Rectangle, c : Color):
        pygame.draw.rect(self.screen, c.tuple, r.tuple)

    def button(self, b : Button):
        self.rectangle(b.rectangle, b.color)

    def text(self, t : Text):
        surface = self.font.render(t.text, True, (0, 0, 0))
        rectangle = surface.get_rect(topleft=(t.x, t.y))
        self.screen.blit(surface, rectangle)

    def loop(self):
        while True:
            self.click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.click = True

            pygame.display.flip()
            self.mouse = pygame.mouse.get_pos()
            self.screen.fill(Window.background.tuple)
            self.game.update(Point(self.mouse[0], self.mouse[1]), self.click)

            for pipe in self.game.pipes:
                for rectangle in pipe.rectangles:
                    self.rectangle(rectangle, pipe.color)

            for bird in self.game.birds:
                angled = pygame.transform.rotate(self.sprites[Bird.sprite], bird.velocity * 10)
                rectangle = angled.get_rect(center=pygame.Rect(bird.rectangles[0].tuple).center)
                self.image(angled, rectangle)
 
            for button in self.game.buttons:
                self.button(button)
            for text in self.game.texts:
                self.text(text)

            self.image(self.sprites[self.game.ground.sprite], self.game.ground.rectangles[0].tuple)

    def run(self):
        self.loop()


