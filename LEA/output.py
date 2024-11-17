from pynput.mouse import Controller

class PreDefinedMovements:
    def __init__(self):
        self.mouse = Controller()
    
    def move_left(self):
        self.mouse.position = (self.mouse.position[0] - 3, self.mouse.position[1])

    def move_right(self):
        self.mouse.position = (self.mouse.position[0] + 3, self.mouse.position[1])

    def move_up(self):
        self.mouse.position = (self.mouse.position[0], self.mouse.position[1] + 3)

    def move_down(self):
        self.mouse.position = (self.mouse.position[0], self.mouse.position[1] - 3)

    def click(self):
        self.mouse.click()

if __name__ == "__main__":
    thing = PreDefinedMovements()
    thing.move_left()
