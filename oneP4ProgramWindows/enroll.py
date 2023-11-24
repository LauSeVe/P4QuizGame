from PyQt5.QtWidgets import QWidget, QLabel

class EnrollWindow(QWidget):

    # Initialize Enroll Window
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT):
        super().__init__()
        
        # Enroll Window Setup
        self.setWindowTitle("Enrollment")
        self.setGeometry(SCREEN_WIDTH//2-WINDOW_WIDTH//2, SCREEN_HEIGHT//2-WINDOW_HEIGHT//2, WINDOW_WIDTH, WINDOW_HEIGHT)

        # Title Label
        title = QLabel("TO-DO", self)
        title.setStyleSheet("font-size: 30px; font-weight: bold;")
        title.move(WINDOW_WIDTH//2 - title.width()//2, WINDOW_HEIGHT//2 - title.height()//2)
