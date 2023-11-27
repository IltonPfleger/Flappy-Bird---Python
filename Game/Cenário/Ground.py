from Utils import Rectangle, Color, Window

class Ground:
    sprite = "Images/ground.png"
    def __init__(self):
        height = 100
        self.rectangles = [Rectangle(0, Window.height - height, Window.width, height)]
