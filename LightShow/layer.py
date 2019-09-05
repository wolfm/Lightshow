class Layer:

    #pixels = []
    #num_pixels = 0
    #update_set = set()
    #effect = None
    #layer_level = 0

    def __init__(self, num_pixels, effect_in, layer_level_in, end_time_in):
        self.num_pixels = num_pixels
        self.effect = effect_in
        self.layer_level = layer_level_in
        self.pixels = [(0,0,0,0)] * num_pixels
        self.end_time = end_time_in
        self.update_set = set()

    def __getitem__(self, index):
        return self.pixels[index]

    def __setitem__(self, index, value):
        self.pixels[index] = value
        self.update_set.add(index)

    def get_update_set(self):
        return self.update_set

    def clear_update_set(self):
        self.update_set.clear()
    
    def getEffect(self):
        return self.effect

    def getLayerLevel(self):
        return self.layer_level

    def start(self):
        self.effect.start(self, self.num_pixels)

    def update_layer(self, currentTime):
        self.effect.render(self, self.num_pixels, currentTime)
        return self.update_set

    def fill(self, color, start_index = 0, end_index = -1):
        #a bad temporary solution for not being able to use self.num_pixels as default value
        if end_index == -1: end_index = self.num_pixels

        for i in range(start_index, end_index):
            self.update_set.add(i)
            self.pixels[i] = color