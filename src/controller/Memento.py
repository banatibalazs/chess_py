import copy

class Memento:
    def __init__(self, state):
        self._state = copy.deepcopy(state)

    def get_state(self):
        return self._state

class Caretaker:
    def __init__(self):
        self._mementos = []

    def add_memento(self, memento):
        self._mementos.append(memento)

    def get_memento(self, index):
        return self._mementos[index]

class ChessGame:
    def __init__(self):
        self._state = {}
        self._caretaker = Caretaker()

    def set_state(self, state):
        self._state = state

    def save_state(self):
        memento = Memento(self._state)
        self._caretaker.add_memento(memento)

    def restore_state(self, index):
        memento = self._caretaker.get_memento(index)
        self._state = memento.get_state()