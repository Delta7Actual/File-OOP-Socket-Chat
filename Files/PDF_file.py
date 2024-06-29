from Files.base_file import base_file

class PDF_file(base_file):
    def __init__(self, name, size, author, body):
        super().__init__(name,size)
        self.author = author
        self.body = body

    def display(self):
        return f"File: {self.name} - Size: {self.size} - Author: {self.author} - body: {self.body}"
