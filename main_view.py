import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QMessageBox, QAbstractItemView, QProgressBar, QTableWidgetItem, \
    QColorDialog, QTableWidget

from custom_signals import CustomSignals
from device_interaction import *
from dynamicsDialog_view import DynamicsDialog
from graph_view import barplot_pids_pagemap
from handling.device_handler import DeviceHandler
from handling.listener import Listener
from pages_graphics import plot_pids_pagemap
from picture_view import PhotoViewer
from qt_ui.mainWindow_ui import Ui_MainWindow
from selectDialog_view import SelectDialog
from tableDialog_view import TableDialog
from tree_dialog.treeDialogFacade import TreeDialogFacade
from tree_dialog.treeDialog_view import TreeDialog
from utilities import *


class MainView(QMainWindow, Listener):
    def __init__(self):
        super().__init__()
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self.devices_handler = DeviceHandler()
        self.devices_handler.add_listener(self)
        self.device_interaction = DeviceInteraction()
        self.signals = CustomSignals()
        self._ui.tableWidget.verticalHeader().setVisible(False)
        self.set_buttons(pid=False, data=False, nxt=False, prev=False, play=False, cgr=False, refc=False,
                         highlight=False)

        self.pages_stats_graph = PhotoViewer(need_zoom=False, parent=self._ui.graphicsBar)
        layout = QVBoxLayout(self._ui.graphicsBar)
        layout.addWidget(self.pages_stats_graph)
        self._ui.graphicsBar.setStyleSheet("background-color: whitesmoke")

        self.pages_graph = PhotoViewer(need_zoom=True, parent=self._ui.graphicsPresent)
        layout = QVBoxLayout(self._ui.graphicsPresent)
        layout.addWidget(self.pages_graph)
        self._ui.graphicsPresent.setStyleSheet("background-color: whitesmoke")

        self._ui.dataButton.clicked.connect(self.collect_data)
        self._ui.pidsButton.clicked.connect(self.select_processes)
        self._ui.actionShow_CGroup_tree.triggered.connect(self.select_processes_cgroup)
        self._ui.devicesButton.clicked.connect(self.select_devices)
        self._ui.playButton.clicked.connect(self.mem_dynamics)
        self._ui.prevButton.clicked.connect(self.mem_prev_state)
        self._ui.nextButton.clicked.connect(self.mem_next_state)
        self._ui.highlightButton.clicked.connect(self.highlight_pids)
        self._ui.refreshColorsButton.clicked.connect(self.refresh_colors)
        self._ui.tableWidget.customContextMenuRequested.connect(self.call_menu)

        self._ui.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        self.timer = QtCore.QTimer()
        self.time = QtCore.QTime(0, 0, 0)

        self.timer.timeout.connect(self.timer_event)
        self.timer.start(1000)

        self.devices_handler.update()

        self.active_pids = []
        self.active_state = -1
        self.active_pids_len = 0
        self.iteration_time = 0
        self.total_time = 0
        self.is_data_collected = False

    def call_menu(self, point):
        if self.active_state == -1:
            return
        menu = QtWidgets.QMenu()
        info_action = menu.addAction("Show full information")
        color_action = menu.addAction("Change color")
        info_action.triggered.connect(self.show_pid_info)
        color_action.triggered.connect(self.change_pid_color)
        menu.exec(self._ui.tableWidget.mapToGlobal(point))

    def show(self):
        super().show()
        self._ui.devicesButton.clicked.emit()

    def update_data(self):
        self.device_interaction.clear()
        if not self.devices_handler.is_device_selected():
            return

        try:
            self.device_interaction.collect_pid_list_all()
            self.device_interaction.collect_cgroups_list()
        except CalledProcessError:
            self.show_msg('Error', 'Check connection with device and tool presence')
        except EmptyDataError:
            self.show_msg('Error', 'Pid list unavailable')
        finally:
            clean_tmp_data_from_device(device=self.devices_handler.get_device(), remove_page_data=False)
            clean_tmp_data(remove_page_data=False, remove_pictures_data=False)

    def generate_pid_colors(self, update_active_pids=True):
        for i in range(self.active_pids_len):
            if self.active_pids[i]['corrupted']:
                self.active_pids[i]['color'] = QColor(Qt.transparent)
            elif update_active_pids:
                alpha, self.active_pids[i]['color'] = self.active_pids[i]['color'].alpha(), generate_color()
                self.active_pids[i]['color'].setAlpha(alpha)
            self.set_table_color(i)

    def display_page_data(self):
        try:
            iterations = self.device_interaction.get_iterations()
            if iterations is not None:
                for i in range(iterations):
                    self.plot_page_data(i)
        except AttributeError:
            pass  # no data collected yet
        finally:
            clean_tmp_data_from_device(device=self.devices_handler.get_device(), remove_pids_data=False)
            clean_tmp_data(remove_pictures_data=False, remove_pids_data=False)

    def refresh_colors(self):
        self.generate_pid_colors()
        self.display_page_data()
        self.show_state(self.active_state)

    def view_checked_pids(self, checked_pids):
        self._ui.tableWidget.clear()
        row = len(checked_pids)
        col = 2
        self._ui.tableWidget.setColumnCount(col)
        self._ui.tableWidget.setRowCount(row)

        self.active_pids = []

        for i in range(row):
            self.active_pids.append({
                'pid': checked_pids[i][0],
                'title': checked_pids[i][1],
                'corrupted': False,
                'highlighted': True,
                'color': generate_color()
            })
            for j in range(col):
                item = QTableWidgetItem()
                if j == 0:
                    item.setCheckState(Qt.Unchecked)
                item.setText(str(checked_pids[i][j]))
                self._ui.tableWidget.setItem(i, j, item)

        self.active_pids_len = len(self.active_pids)

        self._ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._ui.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self._ui.tableWidget.horizontalHeader().setStretchLastSection(True)
        self._ui.tableWidget.horizontalHeader().hide()
        self._ui.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self._ui.tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.is_data_collected = False

    def timer_event(self):
        self.time = self.time.addSecs(1)
        self.timer.start(1000)
        self.devices_handler.update()
        if self.time.second() % 30 == 0:
            self.react()

    def show_msg(self, msg_type, msg):
        QGuiApplication.restoreOverrideCursor()
        QMessageBox.about(self, msg_type, msg)

    def closeEvent(self, event):
        clean_tmp_data_from_device(device=self.devices_handler.get_device())
        clean_tmp_data()
        event.accept()

    def react(self):
        super().react()
        if not self.devices_handler.is_device_selected():
            self.view_checked_pids([])
            self.set_buttons(pid=False, data=False, refc=False, highlight=False)
        self.set_buttons()
        self.update_data()
        self.signals.pids_changed.emit(self.device_interaction.get_pid_list_all())
        self.signals.devices_changed.emit(self.devices_handler.devices_list())
        self.signals.cgroup_changed.emit(self.device_interaction.get_cgroups_list())

    def show_state(self, state_index):
        self.pages_graph.set_item(QtGui.QPixmap(f'resources/data/pictures/offsets/p{state_index}.png'))
        self.pages_stats_graph.set_item(QtGui.QPixmap(f'resources/data/pictures/barplot/b{state_index}.png'))
        self.set_buttons(prev=(self.active_state > 0),
                         nxt=(self.active_state < self.device_interaction.get_iterations() - 1))

    @pyqtSlot()
    def collect_data(self):
        if not self.devices_handler.is_device_selected():
            self.show_msg('Error', 'No attached devices')
            return

        self.pages_graph.set_content(False)
        self.set_buttons(data=False, refc=False, highlight=False)
        progress = QProgressBar(self)
        progress.move(self._ui.centralWidget.geometry().center())

        dynamics_dialog = DynamicsDialog()
        dynamics_dialog.signals.send_data.connect(self.set_collection_time)
        dynamics_dialog.exec_()

        if self.iteration_time < 0 or self.total_time <= 0:
            self.show_msg('Error', 'Please enter the other number of iterations')
            self.set_buttons(data=True, refc=True)
            return

        iterations = 0
        self.device_interaction.set_iterations(iterations)

        QGuiApplication.setOverrideCursor(Qt.WaitCursor)
        progress.show()
        start_time = time.time()
        cur_time = start_time
        error_pids = []
        while cur_time - start_time <= self.total_time:
            try:
                pid_list = [pid['pid'] for pid in self.active_pids]
                error_pids = self.device_interaction.collect_page_data(cur_iteration=iterations, pid_list=pid_list)
            except Exception:
                self.show_msg('Error', 'Either the process is a system process (no access) or it has already completed,'
                                       'also check tool presence')
                progress.hide()
                self.set_buttons(data=False)
                return

            iterations += 1
            self.device_interaction.set_iterations(iterations)
            sleep(self.iteration_time)
            cur_time = time.time()
            progress.setValue((cur_time - start_time) * 100 // self.total_time)

        for index, pid in enumerate(self.active_pids):
            if pid['pid'] in error_pids:
                pid['corrupted'] = True
                self._ui.tableWidget.item(index, 0).setCheckState(Qt.Unchecked)

        # drawing all data after collecting to detect corrupted pids
        # and draw at the same time
        self.generate_pid_colors(update_active_pids=True if not self.is_data_collected else False)
        self.display_page_data()

        progress.setValue(100)
        QGuiApplication.restoreOverrideCursor()
        progress.hide()

        # display first state after collecting data
        self.active_state = 0
        self.show_state(self.active_state)
        self.set_buttons(data=True, refc=True, highlight=True)
        self.set_buttons(prev=(self.active_state > 0),
                         nxt=(self.active_state < self.device_interaction.get_iterations() - 1),
                         play=True)
        self.is_data_collected = True

    def plot_page_data(self, iteration):
        color_list = []
        highlighted_pid_list = []
        for pid in list(filter(lambda el: el['corrupted'] is False, self.active_pids)):
            if pid['highlighted'] is True:
                highlighted_pid_list.append(pid['pid'])
            color_list.append(pid['color'])

        page_data = (self.device_interaction.get_page_data(iteration, present=True),
                     self.device_interaction.get_page_data(iteration, swapped=True))

        plot_pids_pagemap(page_data, color_list, iteration)

        barplot_pids_pagemap(self.device_interaction.get_page_data(iteration),
                             highlighted_pid_list,
                             str(iteration))

    @pyqtSlot()
    def mem_dynamics(self):
        self.active_state = 0
        for i in range(self.device_interaction.get_iterations()):  # simple implementation using sleep
            self._ui.nextButton.clicked.emit()
            self.set_buttons(prev=False, nxt=False)
            sleep(0.5)
        self.set_buttons(prev=(self.active_state > 0),
                         nxt=(self.active_state < self.device_interaction.get_iterations() - 1),
                         play=True)

    @pyqtSlot()
    def mem_prev_state(self):
        if self.active_state > 0:
            self.active_state -= 1
            self.show_state(self.active_state)

    @pyqtSlot()
    def mem_next_state(self):
        if self.active_state < self.device_interaction.get_iterations() - 1:
            self.active_state += 1
            self.show_state(self.active_state)

    @pyqtSlot(object)
    def set_active_pids(self, data):
        self.view_checked_pids(data)
        self.set_buttons(data=True if self.active_pids_len > 0 else False,
                         refc=False,
                         highlight=False)

    @pyqtSlot(object)
    def set_collection_time(self, data):
        self.iteration_time = data[0] if data is not None else -1
        self.total_time = data[1] if data is not None else -1

    @pyqtSlot(object)
    def set_device_data(self, data):
        if len(data) > 0:
            self.devices_handler.switch(str(data[0][0]))
            self.device_interaction.set_device(self.devices_handler.get_device())
            self.set_buttons(pid=True, cgr=True)

        self._ui.statusBar.showMessage(f'{data[0][0] if len(data) > 0 else "No"} device was connected')
        self.react()

    @pyqtSlot()
    def select_processes(self):
        pids_dialog = SelectDialog(data_list=self.device_interaction.get_pid_list_all(),
                                   label='Select pids',
                                   has_select_all=True,
                                   parent=self)
        self.signals.pids_changed.connect(pids_dialog.update)
        pids_dialog.signals.send_data.connect(self.set_active_pids)
        pids_dialog.exec_()

    @pyqtSlot()
    def select_devices(self):
        devices_dialog = SelectDialog(data_list=self.devices_handler.devices_list(),
                                      label='Select devices',
                                      close_on_detach=False,
                                      parent=self)
        self.signals.devices_changed.connect(devices_dialog.update)
        devices_dialog.signals.send_data.connect(self.set_device_data)
        devices_dialog.exec_()

    @pyqtSlot()
    def show_pid_info(self):
        pid_index = self._ui.tableWidget.selectedIndexes()[0].row()
        pid = self.active_pids[pid_index]['pid']
        if self.active_pids[pid_index]['corrupted']:
            self.show_msg('Message', 'No access to the process data')
            return
        try:
            data_frame = self.device_interaction.get_page_data(self.active_state).get(pid)
            table_dialog = TableDialog(pid, data_frame.values)
            table_dialog.exec_()
        except Exception:
            self.show_msg('Message', 'Data hasn\'t been collected yet')

    @pyqtSlot()
    def select_processes_cgroup(self):
        tree_dialog = TreeDialog(self.device_interaction.get_cgroups_list())
        transfer_data_facade = TreeDialogFacade(self.device_interaction, tree_dialog)
        self.signals.cgroup_changed.connect(tree_dialog.update)
        tree_dialog.signals.send_data.connect(self.set_active_pids)
        tree_dialog.signals.cgroup_data_request.connect(transfer_data_facade.transfer_data)
        tree_dialog.exec_()

    def set_buttons(self, pid=None, data=None, nxt=None, prev=None, play=None, cgr=None, refc=None, highlight=None):
        self._ui.pidsButton.setEnabled(pid if pid is not None else self._ui.pidsButton.isEnabled())
        self._ui.dataButton.setEnabled(data if data is not None else self._ui.dataButton.isEnabled())
        self._ui.nextButton.setEnabled(nxt if nxt is not None else self._ui.nextButton.isEnabled())
        self._ui.prevButton.setEnabled(prev if prev is not None else self._ui.prevButton.isEnabled())
        self._ui.playButton.setEnabled(play if play is not None else self._ui.playButton.isEnabled())
        self._ui.actionShow_CGroup_tree.setEnabled(
            cgr if cgr is not None else self._ui.actionShow_CGroup_tree.isEnabled())
        self._ui.refreshColorsButton.setEnabled(
            refc if refc is not None else self._ui.refreshColorsButton.isEnabled())
        self._ui.highlightButton.setEnabled(
            highlight if highlight is not None else self._ui.highlightButton.isEnabled())

    def change_pid_color(self):
        index = self._ui.tableWidget.selectedIndexes()[0].row()
        if self.active_pids[index]['corrupted']:
            return
        alpha, self.active_pids[index]['color'] = self.active_pids[index]['color'].alpha(), \
                                                  QColorDialog.getColor()
        self.active_pids[index]['color'].setAlpha(alpha)
        self.set_table_color(index)
        self.display_page_data()
        self.show_state(self.active_state)

    # edit alpha component for every picture for given index of pid
    def edit_alpha(self, pid_table_index, alpha):
        self.active_pids[pid_table_index]['color'].setAlpha(alpha)
        self.set_table_color(pid_table_index)

    # set color components according to table
    def set_table_color(self, pid_table_index):
        columns = 2
        for col in range(columns):
            self._ui.tableWidget.item(pid_table_index, col).setBackground(
                QBrush(self.active_pids[pid_table_index]['color']))
        if self.active_pids[pid_table_index]['corrupted']:
            self._ui.tableWidget.item(pid_table_index, 0).setCheckState(Qt.Unchecked)
            self._ui.tableWidget.item(pid_table_index, 0).setFlags(QtCore.Qt.ItemIsEnabled)

    @pyqtSlot()
    def highlight_pids(self):
        for index in range(self.active_pids_len):
            if self._ui.tableWidget.item(index, 0).checkState() == Qt.Unchecked:
                self.active_pids[index]['highlighted'] = False
                if not self.active_pids[index]['corrupted']:
                    self.edit_alpha(index, 40)  # make dim
            else:
                self.active_pids[index]['highlighted'] = True
                self.edit_alpha(index, 255)  # make highlighted
        self.display_page_data()
        self.show_state(self.active_state)
