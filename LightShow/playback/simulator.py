from tkinter import *
import time
from collections import deque

class Simulator:

    canvas_width = 800
    canvas_height = 76

    pixels = []
    master = 0
    w = 0
    y = int(canvas_height / 2)
    pixel_width = 0
    pixel_pos_list = []
    num_pixels = 0
    rectangles = []

    update_queue = deque()

    def __init__(self, num_pixels):


        self.num_pixels = num_pixels

        self.master = Tk()

        self.pixel_width = self.canvas_width / self.num_pixels

        self.w = Canvas(self.master, 
                width=self.canvas_width,
                height=self.canvas_height)
        self.w.pack()

        for i in range(0, self.num_pixels):
            self.pixels.append((0, 0, 0))
            self.pixel_pos_list.append(i * self.pixel_width)
            rect_left_x = i * self.pixel_width
            self.rectangles.append(self.w.create_rectangle(rect_left_x, self.y, rect_left_x + self.pixel_width, self.y - self.pixel_width, outline="#000000", fill="#000000"))


        self.show()

    def show(self):
        hexcode = '#000000'

        '''
        for i in range(0, self.num_pixels):
            hexcode = '#%02x%02x%02x' % self.pixels[i]
            self.w.itemconfig(self.rectangles[i] , fill=hexcode)

        '''

        while len(self.update_queue) > 0:
            item = self.update_queue.popleft()
            hexcode = '#%02x%02x%02x' % item[1]
            self.w.itemconfig(self.rectangles[item[0]], fill = hexcode)            
        
        #Tkinter GUI update
        self.master.update_idletasks()
        self.master.update()

    def fill(self, color):
        for i in range(0, self.num_pixels):
            self[i] = color

    def __getitem__(self, index):
        return self.pixels[index]

    def __setitem__(self, index, value):
        self.pixels[index] = value
        self.update_queue.append((index, value))
