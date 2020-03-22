from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtWidgets import QGraphicsView


class PictureViewer(QGraphicsView):
    """Widget for displaying plotted graphs on QGraphicsScene
    :ivar scene: QGraphicsScene to draw pictures
    :ivar pixmap_content: pixmap containing picture's representation
    :ivar zoom: zoom ratio
    :ivar has_content: flag indicating if picture is set
    :ivar has_zoom: flag indicating if zoom is enabled
    """
    def __init__(self, need_zoom=False, parent=None):
        super(PictureViewer, self).__init__(parent)
        self.scene = QtWidgets.QGraphicsScene(self)
        self.pixmap_content = QtWidgets.QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_content)
        self.setScene(self.scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.zoom = 0
        self.has_content = False
        self.has_zoom = need_zoom

    def fitInView(self):
        super().fitInView(QRectF(self.pixmap_content.pixmap().rect()), Qt.IgnoreAspectRatio)

    def set_content(self, flag):
        self.has_content = flag
        self.zoom = 0

    def set_item(self, picture: QtGui.QPixmap):
        if picture and not picture.isNull():
            self.pixmap_content.setPixmap(picture)
        else:
            self.pixmap_content.setPixmap(QtGui.QPixmap())

        # Assuming all pictures have same size so setup for first
        if not self.has_content:
            self.fitInView()
            self.has_content = True

    def wheelEvent(self, event: QtGui.QWheelEvent):
        if not self.has_zoom:
            event.ignore()
            return
        # Zoom Factor
        zoom_in_factor = 1.25
        zoom_out_factor = 1 / zoom_in_factor

        # Set Anchors
        self.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.setResizeAnchor(QGraphicsView.NoAnchor)

        # Save the scene pos
        old_pos = self.mapToScene(event.pos())

        # Zoom
        if event.angleDelta().y() > 0:
            self.zoom += 1
            zoom_factor = zoom_in_factor
        else:
            zoom_factor = zoom_out_factor
            self.zoom -= 1

        if 0 <= self.zoom <= 15:
            self.scale(zoom_factor, zoom_factor)

        # Set bounds for zooming
        if self.zoom > 15:
            self.zoom = 15
        elif self.zoom < 0:
            self.zoom = 0

        # Get the new position
        new_pos = self.mapToScene(event.pos())

        # Move scene to old position
        delta = new_pos - old_pos
        self.translate(delta.x(), delta.y())
        event.accept()
