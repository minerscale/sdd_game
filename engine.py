import numpy as np

class Engine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Define screen
        self.screen = np.asarray([[' '] * self.width for i in range(self.height)])
        self.frame = 0

    def draw_text_box(self, x, y, w, h, text='', fill=False):
        if fill:
            self.screen = self.blit(self.screen, [[' '] * w for i in range(h)], (y,x))

        self.screen[y][x]     = '╔'
        self.screen[y][x+w]   = '╗'
        self.screen[y+h][x]   = '╚'
        self.screen[y+h][x+w] = '╝'
        for i in range(w - 1):
            self.screen[y][x+i+1]   = '═'
            self.screen[y+h][x+i+1] = '═'
        
        for i in range(h - 1):
            self.screen[y+i+1][x]   = '║'
            self.screen[y+i+1][x+w] = '║'

        if text != '':
            for i,line in enumerate(text.split('\n')):
                for j,char in enumerate(line):
                    self.screen[y + 1 + i][x + 1 + j] = char

    def flush(self):
        self.screen = [[' '] * self.width for i in range(self.height)]

    def draw(self):
        # Turn screen data into a string
        output = '--------------Make the terminal small enough to hide this message!--------------'
        for i in range(self.height):
            output += "\n" + ''.join(map(str, self.screen[i]))
        # Print the frame
        print (output)

        # Flush the screen
        self.flush()

        self.frame += 1

    def blit(self, a, b, offsets=(0,), transparent_char='α'):
        """
        a: an array object or a tuple is as_shape is True
        b: an array object or a tuple is as_shape is True
        offsets: a sequence of offsets

        return: a multidimensional slice for <a> followed by a multidimensional slice for <b>
        """
    
        # Retrieve and check the array shapes and offset
        a, b = np.array(a, copy=False), np.array(b, copy=False)
        a_shape, b_shape = a.shape, b.shape

        n = min(len(a_shape), len(b_shape))
        if n == 0:
            raise ValueError("Cannot overlap with an empty array")
        offsets = tuple(offsets) + (0,) * (n - len(offsets))
        if len(offsets) > n:
            raise ValueError("Offset has more elements than either number of dimensions of the arrays")
    
        # Compute the slices
        a_slices, b_slices = [], []
        for i, (a_size, b_size, offset) in enumerate(zip(a_shape, b_shape, offsets)):
            a_min = max(0, offset)
            a_max = min(a_size, max(b_size + offset, 0))
            b_min = max(0, -offset)
            b_max = min(b_size, max(a_size - offset, 0))
            a_slices.append((a_min, a_max))
            b_slices.append((b_min, b_max))
    
        a_slice, b_slice = tuple(a_slices), tuple(b_slices)

        # Print the slices with transparency
        for y in range(b_slice[0][0], b_slice[0][1]):
            for x in range(b_slice[1][0], b_slice[1][1]):
                if (b[y][x] != transparent_char):
                    a[y + a_slice[0][0]][x + a_slice[1][0]] = b[y][x]
        return a

if __name__ == '__main__':
    import image
    import time

    class Game(Engine):
        def __init__(self):
            Engine.__init__(self, 80, 23)
            self.DVD = image.convert('dvd.txt')
            self.x_pos = 0
            self.y_pos = 0
            self.x_vel = 1
            self.y_vel = 1

        def run(self):
            self.x_pos += self.x_vel
            self.y_pos += self.y_vel
            if self.x_pos <= 0 or self.x_pos >= self.width - self.DVD.w:
                self.x_vel = -self.x_vel
            if self.y_pos <= 0 or self.y_pos >= self.height - self.DVD.h:
                self.y_vel = -self.y_vel

            self.screen = self.blit(self.screen, self.DVD.data, (self.y_pos, self.x_pos))
            self.draw()

    game = Game()
    while(1):
        game.run()
        time.sleep(1/12)
