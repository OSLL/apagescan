from PyQt5.QtWidgets import QDialog

from qt_models.pagemapModel import PagemapModel
from qt_ui.tableDialog_ui import Ui_TableDialog


class TableDialog(QDialog):
    def __init__(self, pid, pages_list):
        super(TableDialog, self).__init__()

        self.pid = pid
        self.pages_list = pages_list
        self._ui = Ui_TableDialog()
        self._ui.setupUi(self)

        self._ui.pidLineEdit.setText(str(pid))

        self.pagemap_model = PagemapModel(self.pages_list)
        self._ui.pidTableView.setModel(self.pagemap_model)
        self._ui.pidTableView.horizontalHeader().setStretchLastSection(True)
