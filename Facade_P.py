"""Facade pattern WashingMachine"""

class Washing: #Стирает
    '''Subsystem # 1'''

    def wash(self):
        print("Washing...")

class Rinsing: #Полоскание
    '''Subsystem # 2'''

    def rinse(self):
        print("Rinsing...")

class Spinning: # Отжим
    '''Subsystem # 3'''

    def spin(self):
        print("Spinning...")


class WashingMachine:
    '''Facade'''

    def __init__(self):
        self.washing = Washing()
        self.rinsing = Rinsing()
        self.spinning = Spinning()

    def startWashing(self):
        self.washing.wash()
        self.rinsing.rinse()
        self.spinning.spin()

""" main method """
if __name__ == "__main__":

    washingMachine = WashingMachine()
    washingMachine.startWashing()
