# this class does not inherit from model, it is just a node to be in a tree
class PidNode(object):
    """Node element for PidTreeModel
    """

    def __init__(self, pid=-1, parent=None):
        self.pid = pid
        self.parent = parent
        self.children = []
        self.set_parent(parent)

    def set_parent(self, parent):
        if parent is not None:
            self.parent = parent
            self.parent.append_child(self)
        else:
            self.parent = None

    def append_child(self, child):
        self.children.append(child)

    def child_at_row(self, row):
        return self.children[row]

    def row_of_child(self, child):
        return self.children.index(child)

    def remove_child(self, row):
        value = self.children[row]
        self.children.remove(value)
        return True

    def __len__(self):
        return len(self.children)
