class ViewModel:

    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items

    @property
    def todo_items(self):
        return [item for item in self._items if item.listName == 'To Do']

    @property
    def doing_items(self):
        return [item for item in self._items if item.listName == 'Doing']

    @property
    def done_items(self):
        return [item for item in self._items if item.listName == 'Done']

    