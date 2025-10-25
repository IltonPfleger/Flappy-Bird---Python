from Utils import Rectangle, Color, Window, Image

class Ground:
    sprite = "Images/ground.png"
    height = 100
    def __init__(self):
        self.image = Image(Ground.sprite, Rectangle(0, Window.height - Ground.height, Window.width, Ground.height))
