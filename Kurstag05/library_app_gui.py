import sys

from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTableWidget,
                             QTableWidgetItem, QWidget, QMessageBox)
from PyQt5.QtCore import Qt


class Book:
    def __init__(self, title, author, is_available=True):
        self.title = title
        self.author = author
        self.is_available = is_available


class LibraryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Buchausleihsystem TEKO")
        self.setGeometry(100, 100, 550, 500)

        self.books = [
            Book("1984", "George Orwell"),
            Book("To Kill a Mockingbird", "Harper Lee", is_available=False),
            Book("The Great Gatsby", "F. Scott Fitzgerald"),
        ]

        self.book_table = None
        self.new_title = None
        self.new_author = None
        self.add_button = None
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Header
        header = QLabel("Buchausleihsystem TEKO")
        header.setStyleSheet("font-size: 20px; font-weight: bold;")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # Book table
        self.book_table = QTableWidget()
        self.book_table.setColumnCount(3)
        self.book_table.setHorizontalHeaderLabels(["Titel", "Autor", "Status"])
        self.populate_book_table()
        self.book_table.cellDoubleClicked.connect(self.on_toggle_available)  # type: ignore
        layout.addWidget(self.book_table)

        # Add new book inputs
        input_layout = QHBoxLayout()

        self.new_title = QLineEdit()
        self.new_title.setPlaceholderText("Titel")
        self.new_title.textChanged.connect(self.on_text_change)  # type: ignore

        self.new_author = QLineEdit()
        self.new_author.setPlaceholderText("Autor")
        self.new_author.textChanged.connect(self.on_text_change)  # type: ignore

        self.add_button = QPushButton("Hinzufügen")
        self.add_button.clicked.connect(self.on_add_book)  # type: ignore
        self.add_button.setEnabled(False)

        input_layout.addWidget(self.new_title)
        input_layout.addWidget(self.new_author)
        input_layout.addWidget(self.add_button)

        layout.addLayout(input_layout)

    def populate_book_table(self):
        self.book_table.setRowCount(len(self.books))
        for row, book in enumerate(self.books):
            self.book_table.setItem(row, 0, QTableWidgetItem(book.title))
            self.book_table.setItem(row, 1, QTableWidgetItem(book.author))
            status = "Verfügbar" if book.is_available else "Ausgeliehen"
            self.book_table.setItem(row, 2, QTableWidgetItem(status))

    def on_add_book(self):
        title = self.new_title.text().strip()
        author = self.new_author.text().strip()

        if title and author:
            self.books.append(Book(title, author))
            self.populate_book_table()
            self.new_title.clear()
            self.new_author.clear()
        else:
            QMessageBox.warning(self, "Fehler", "Bitte sowohl Titel als auch Autor eingeben.")

    def on_toggle_available(self, row):
        book = self.books[row]
        book.is_available = not book.is_available
        self.populate_book_table()

    def on_text_change(self):
        if self.new_title.text().strip() and self.new_author.text().strip():
            self.add_button.setEnabled(True)
        else:
            self.add_button.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LibraryApp()
    window.show()
    sys.exit(app.exec_())
