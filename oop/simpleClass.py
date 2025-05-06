# Define the class
class Worker:
    # Define how a worker is initialized
    def __init__(self,  is_working=True, num_reprimands=0):
        # Set its data (aka variables or attributes)
        self.is_working = is_working
        self.num_reprimands = num_reprimands

    # define its functions (aka methods or behavior)
    def hide_from_boss(self):
        print(f"{self.name} is hiding from the boss.")
        self.is_working = False

    def act_like_working(self):
        print(f"{self.name} is pretending to work.")
        self.is_working += 1

# Instantiating the object
Steve = Worker(is_working=False, num_reprimands=2)

# Using methods
Steve.hide_from_boss()
Steve.act_like_working()




