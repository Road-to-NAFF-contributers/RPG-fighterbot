from interactions import *


class CustomExtension(Extension):
    # Init function – runs when the extension is loaded
    def __init__(self, bot):
        print(f"Extension {self.name} loaded")
