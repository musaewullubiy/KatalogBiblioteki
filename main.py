import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QDialog, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5 import uic


class Program(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui.ui', self)
        self.con = sqlite3.connect('books_info.sqlite')
        self.cur = self.con.cursor()
        self.temp_wids = list()

        self.search_btn.clicked.connect(self.search_books)

    def search_books(self):
        search_text = self.search_text.text()
        if search_text != '':
            for i in self.temp_wids:
                i.hide()
                i.destroy()
            self.temp_wids = list()
            if self.search_variant.currentText() == 'Название':
                variant = 'title'
            else:
                variant = 'author'
            data = self.cur.execute(f'SELECT * FROM info WHERE {variant} LIKE \'%{search_text}%\'').fetchall()
            for i in data:
                self.add_buttons(i)
            self.void_for_viz = QLabel(self.book_btns_group_box)
            self.void_for_viz.setObjectName("void_for_viz")
            self.verticalLayout.addWidget(self.void_for_viz)
            self.temp_wids.append(self.void_for_viz)

    def add_buttons(self, data):
        self.book_btn = PushButtonWithData(self.book_btns_group_box)
        self.book_btn.setObjectName("book_btn")
        self.book_btn.set_data(data)
        self.book_btn.setText(data[1])
        self.book_btn.clicked.connect(self.open_dialog)
        self.temp_wids.append(self.book_btn)
        self.verticalLayout.addWidget(self.book_btn)

    def open_dialog(self):
        data = self.sender().get_data()
        self.dialog = BookDialog(data)
        self.dialog.show()


class PushButtonWithData(QPushButton):
    def __init__(self, *args):
        super(PushButtonWithData, self).__init__(*args)

    def set_data(self, data):
        self.data = data

    def get_data(self):
        return self.data


class BookDialog(QDialog):
    def __init__(self, data):
        super(BookDialog, self).__init__()
        self.vbox_layout = QVBoxLayout()

        self.pic = QLabel()
        self.pic.setAlignment(Qt.AlignCenter)
        if data[5] is None:
            self.pic.setPixmap(QPixmap('pics\\nopic_books.jpg'))
        else:
            self.pic.setPixmap(QPixmap(data[5]))
        self.vbox_layout.addWidget(self.pic)
        print(data)

        font = QFont()
        font.setPointSize(26)

        self.title_word_label = QLabel('Название')
        self.title_word_label.setFont(font)
        self.title_word_label.setAlignment(Qt.AlignCenter)
        self.vbox_layout.addWidget(self.title_word_label)

        self.title_label = QLabel(data[1])
        self.title_label.setAlignment(Qt.AlignCenter)
        self.vbox_layout.addWidget(self.title_label)

        self.author_word_label = QLabel('Автор')
        self.author_word_label.setFont(font)
        self.author_word_label.setAlignment(Qt.AlignCenter)
        self.vbox_layout.addWidget(self.author_word_label)

        self.author_label = QLabel(data[2])
        self.author_label.setAlignment(Qt.AlignCenter)
        self.vbox_layout.addWidget(self.author_label)

        self.year_word_label = QLabel('Год выпуска')
        self.year_word_label.setFont(font)
        self.year_word_label.setAlignment(Qt.AlignCenter)
        self.vbox_layout.addWidget(self.year_word_label)

        self.year_label = QLabel(str(data[3]))
        self.year_label.setAlignment(Qt.AlignCenter)
        self.vbox_layout.addWidget(self.year_label)

        self.genre_word_label = QLabel('Жанр')
        self.genre_word_label.setFont(font)
        self.genre_word_label.setAlignment(Qt.AlignCenter)
        self.vbox_layout.addWidget(self.genre_word_label)

        self.genre_label = QLabel(data[4])
        self.genre_label.setAlignment(Qt.AlignCenter)
        self.vbox_layout.addWidget(self.genre_label)
        self.setLayout(self.vbox_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Program()
    ex.show()
    sys.exit(app.exec())