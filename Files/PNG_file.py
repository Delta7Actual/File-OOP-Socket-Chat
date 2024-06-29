from Files.base_file import base_file

class PNG_file(base_file):

    def __init__(self, name, size, resolution):
        super().__init__(name,size)
        self.resolution = resolution

    def display(self):
        return f"File: {self.name} - Size: {self.size} - Resolution: {self.resolution}"