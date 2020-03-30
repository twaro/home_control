class ControlledElement:

    def __init__(self):
        self.online = False

    def switch_on(self):
        self.online = True

    def switch_off(self):
        self.online = False


class Light(ControlledElement):

    def __init__(self):
        super().__init__()


class Blind(ControlledElement):

    def __init__(self):
        super().__init__()



zaslony = Blind()
print(zaslony.online)
zaslony.switch_on()
print(zaslony.online)