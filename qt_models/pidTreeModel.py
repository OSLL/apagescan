from PyQt5.QtCore import Qt, QAbstractItemModel, QVariant, QModelIndex

from tree_dialog.pidNode import PidNode


class PidTreeModel(QAbstractItemModel):
    def __init__(self, parent=None):
        super(PidTreeModel, self).__init__(parent)

        self.treeView = parent
        self.headers = ['pid']
        self.tasks = []

        self.columns = 1
        self.root = PidNode()
        self.used = []

    # fill tree model with nodes from data, data is list of [pid, ppid, name_of_pid]
    def setData(self, data=[]):
        self.root = PidNode()
        node_dict = {}
        self.tasks = []

        if len(data) == 0:
            return

        for d in data:
            node_dict[d[0]] = PidNode(str(d[0]) + ' - ' + d[2])
            self.tasks.append([str(d[0]), str(d[2])])

        for d in data:
            if d[1] == 0:
                node_dict[d[0]].set_parent(self.root)
            else:
                node_dict[d[0]].set_parent(node_dict[d[1]])

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headers[section])
        return QVariant()

    def index(self, row, column, parent):
        node = self.node_from_index(parent)
        return self.createIndex(row, column, node.child_at_row(row))

    def data(self, index, role):
        if role == Qt.DecorationRole:
            return QVariant()

        if role == Qt.TextAlignmentRole:
            return QVariant(int(Qt.AlignTop | Qt.AlignLeft))

        if role != Qt.DisplayRole:
            return QVariant()

        node = self.node_from_index(index)

        if index.column() == 0:
            return QVariant(node.pid)
        else:
            return QVariant()

    def columnCount(self, parent):
        return self.columns

    def rowCount(self, parent):
        node = self.node_from_index(parent)
        if node is None:
            return 0
        return len(node)

    def parent(self, child):
        if not child.isValid():
            return QModelIndex()

        node = self.node_from_index(child)

        if node is None:
            return QModelIndex()

        parent = node.parent

        if parent is None:
            return QModelIndex()

        grandparent = parent.parent
        if grandparent is None:
            return QModelIndex()
        row = grandparent.row_of_child(parent)

        return self.createIndex(row, 0, parent)

    def node_from_index(self, index):
        return index.internalPointer() if index.isValid() else self.root
