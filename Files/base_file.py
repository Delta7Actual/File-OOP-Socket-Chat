class base_file:

    def __init__(self, name, size):
        self.name = name
        self.size = size
    
    def display(self):
        print(f"File: {self.name} - Size: {self.size}")