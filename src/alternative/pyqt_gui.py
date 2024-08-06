# from PyQt5.QtGui import QIcon, QDrag, QPixmap, QPainter
# from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QPushButton, QWidget
# from PyQt5.QtCore import Qt, QMimeData
#
# WHITE_COLOR = "#ffffee"
# BLACK_COLOR = "#5f915f"
# WH_KNIGHT_IMAGE_PATH = "../../resources/images/pieces/wh_knight.png"
#
# class DraggableButton(QPushButton):
#     def mousePressEvent(self, event):
#         if event.button() == Qt.LeftButton and not self.icon().isNull():
#             self.drag_start_position = event.pos()
#         super().mousePressEvent(event)  # Call the parent class's mousePressEvent method
#
#     def mouseMoveEvent(self, event):
#         if not (event.buttons() & Qt.LeftButton):
#             return
#         if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
#             return
#
#         drag = QDrag(self)
#         mimedata = QMimeData()
#
#         mimedata.setImageData(self.icon().pixmap(self.iconSize()))
#         drag.setMimeData(mimedata)
#
#         pixmap = QPixmap(self.iconSize())
#         painter = QPainter(pixmap)
#         painter.drawPixmap(self.rect(), self.grab())
#         painter.end()
#
#         drag.setPixmap(pixmap)
#         drag.setHotSpot(event.pos())
#         drag.exec_(Qt.CopyAction | Qt.MoveAction)
#
#
# class ChessBoard(QMainWindow):
#     def __init__(self, square_size=100):
#         super().__init__()
#
#         self.square_size = square_size
#
#         self.setWindowTitle("Chess Board")
#
#         self.main_widget = QWidget(self)
#         self.setCentralWidget(self.main_widget)
#
#         self.grid = QGridLayout(self.main_widget)
#         self.grid.setSpacing(0)  # Set the spacing to 0
#
#         self.init_ui()
#
#     def init_ui(self):
#         for row in range(8):
#             for col in range(8):
#                 button = DraggableButton()
#                 button.setFixedSize(self.square_size, self.square_size)
#                 button.clicked.connect(lambda _, i=row, j=col: self.on_button_clicked(i, j))  # Pass row and column to the function
#                 if row == 0 and col == 0:  # If it's the first square
#                     button.setIcon(QIcon(WH_KNIGHT_IMAGE_PATH))  # Set the image
#                     button.setIconSize(button.size())  # Set the icon size to match the button size
#                 if (row + col) % 2 == 0:
#                     button.setStyleSheet(f"background-color: {WHITE_COLOR}")
#                 else:
#                     button.setStyleSheet(f"background-color: {BLACK_COLOR}")
#                 self.grid.addWidget(button, row, col)
#
#     def on_button_clicked(self, row, col):
#         print(f"Button at ({row}, {col}) clicked!")
#
# if __name__ == "__main__":
#     app = QApplication([])
#     chess_board = ChessBoard()
#     chess_board.show()
#     app.exec_()