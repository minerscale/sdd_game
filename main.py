import numpy as np
import sys

from engine import Engine
import image

class Game(Engine):
    def __init__(self):
        Engine.__init__(self, 80, 23)

        self.man_pos_x = 30
        self.man_pos_y = 5

        self.dvd_pos_x = 0
        self.dvd_pos_y = 0
        self.dvd_speed_x = 1
        self.dvd_speed_y = 1

        # Images!
        self.DVD = image.convert('dvd.txt')
        self.orang = image.convert('orang.txt')
        self.man = image.convert('man.txt')

        # Text processing
        self.prev_command = ''

    def run(self, command):
        # Do all the calculations and graphics
        self.process_input(command)
        self.move_dvd()
        self.do_graphics()
        self.draw()

    def process_input(self, command):
        command = command.lower()
        if command == '':
            command = self.prev_command
        # Quit
        if command in ('exit', 'quit'):
            sys.exit()
        # Movement
        elif command == 'w':
            self.move_man(0,-1)
        elif command == 's':
            self.move_man(0,1)
        elif command == 'd':
            self.move_man(1,0)
        elif command == 'a':
            self.move_man(-1,0)
        elif command in ('wd','dw'):
            self.move_man(1,-1)
        elif command in ('wa','aw'):
            self.move_man(-1,-1)
        elif command in ('sd','ds'):
            self.move_man(1,1)
        elif command in ('sa','as'):
            self.move_man(-1,1)

        self.prev_command = command

    def do_graphics(self):
        # Draw Orang
        self.screen = self.blit(self.screen, self.orang.data, (2, 32))

        # Blit DVD logo
        self.screen = self.blit(self.screen, self.DVD.data, (self.dvd_pos_y, self.dvd_pos_x))

        self.screen = self.blit(self.screen, self.man.data, (self.man_pos_y, self.man_pos_x))
        # Draw a text box
        self.draw_text_box(5, 10, 21, 5,
            text = "   Roses are red,\n  Violets are cool.\n I love text boxes,\nThey're a good tool.",
            fill = True
        )

    def move_dvd(self):
        self.dvd_pos_x += self.dvd_speed_x
        self.dvd_pos_y += self.dvd_speed_y

        if self.dvd_pos_x <= 0 or self.dvd_pos_x >= self.width - self.DVD.w:
            self.dvd_speed_x = -self.dvd_speed_x
        if self.dvd_pos_y <= 0 or self.dvd_pos_y >= self.height - self.DVD.h:
            self.dvd_speed_y = -self.dvd_speed_y

    def move_man(self, x, y):
        # Move x chars horizontally and y chars vertically
        self.man_pos_x += 2*x
        self.man_pos_y += y

        # Move back inside screen
        if self.man_pos_x < 0:
            self.man_pos_x = 0
        elif self.man_pos_x > self.width - self.man.w:
            self.man_pos_x = self.width - self.man.w

        if self.man_pos_y < 0:
            self.man_pos_y = 0
        elif self.man_pos_y > self.height - self.man.h:
            self.man_pos_y = self.height - self.man.h

if __name__ == '__main__':
    game = Game()

    # initial draw call
    game.do_graphics()
    game.draw()
    # Run indenfinitely.
    while (1):
        game.run(input('> '))
