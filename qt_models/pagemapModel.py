from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant


class PagemapModel(QAbstractTableModel):
    def __init__(self, pages_list):
        super(PagemapModel, self).__init__()
        self.pages_list = pages_list
        self.header = ['Address', 'Status', 'Dirty', 'Anon']
        self.visual_data = [lambda x: hex(self.pages_list[x][0]),
                            lambda x: 'Present' if self.pages_list[x][1] == 1 else 'Swapped',
                            lambda x: 'Yes' if self.pages_list[x][2] == 1 else 'No',
                            lambda x: 'Yes' if self.pages_list[x][3] == 1 else 'No',
                            ]

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.pages_list)

    def columnCount(self, parent=None, *args, **kwargs):
        return 4

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.header[section])
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return QVariant(str(section + 1))
        return QVariant()

    def data(self, index, role=None):
        if role == Qt.DisplayRole:
            return self.visual_data[index.column()](index.row())
        else:
            return QVariant()
