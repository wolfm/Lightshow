from tkinter import *
import time
from collections import deque
import sys

class Simulator:

    canvas_width = 800
    canvas_height = 76

    pixels = []
    tk = 0
    canvas = 0
    y = int(canvas_height / 2)
    pixel_width = 0
    pixel_pos_list = []
    num_pixels = 0
    rectangles = []

    update_queue = deque()

    def __init__(self, num_pixels):


        self.num_pixels = num_pixels

        self.tk = Tk()

        self.pixel_width = self.canvas_width / self.num_pixels

        self.canvas = Canvas(self.tk, 
                width=self.canvas_width,
                height=self.canvas_height)
        self.canvas.pack()

        #Create simulated LEDs
        for i in range(0, self.num_pixels):
            self.pixels.append((0, 0, 0))
            self.pixel_pos_list.append(i * self.pixel_width)
            rect_left_x = i * self.pixel_width
            self.rectangles.append(self.canvas.create_rectangle(rect_left_x, self.y, rect_left_x + self.pixel_width, self.y - self.pixel_width, outline="#000000", fill="#000000"))


        self.show()

    def show(self):
        #Initialize hexcode string
        hexcode = '#000000'

        #Iterate through update queue, changing each corresponding pixel
        while len(self.update_queue) > 0:
            item = self.update_queue.popleft()
            hexcode = '#%02x%02x%02x' % item[1]
            self.canvas.itemconfig(self.rectangles[item[0]], fill = hexcode)            
        
        #Tkinter GUI update
        self.tk.update_idletasks()
        self.tk.update()

    def fill(self, color, start_index = 0, end_index = -1):
        #a bad temporary solution for not being able to use self.num_pixels as default value
        if end_index == -1: end_index = self.num_pixels

        for i in range(start_index, end_index):
            self.update_queue.append((i, color))

    def __getitem__(self, index):
        return self.pixels[index]

    def __setitem__(self, index, value):
        self.pixels[index] = value
        self.update_queue.append((index, value))
