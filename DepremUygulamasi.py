import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QTimer
import requests
from bs4 import BeautifulSoup


class EarthquakeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Deprem Uygulaması")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.button = QPushButton("Son Depremleri Görüntüle", self)
        self.button.clicked.connect(self.update_earthquake_data)
        layout.addWidget(self.button)

        # self.text_edit = QTextEdit()
        # self.text_edit.setReadOnly(True)
        # layout.addWidget(self.text_edit)

        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_earthquake_data)
        self.timer.start(10000)  # 10 saniyede bir güncelleme yap


    def update_earthquake_data(self):

        self.button.setEnabled(False)
        
        url = "https://deprem.afad.gov.tr/last-earthquakes.html"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        table = soup.find("table")
        rows = table.find_all("tr")

        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Yer", "Büyüklük", "Derinlik", "Tarih"])
        self.table_widget.setRowCount(len(rows) - 1)
        
        for i, row in enumerate(rows[:101]):
            cells = row.find_all("td")

            if cells:
                location = cells[6].text.strip()
                magnitude = cells[5].text.strip()
                longitude = cells[3].text.strip()
                date = cells[0].text.strip()

                self.table_widget.setItem((i-1), 0, QTableWidgetItem(location))
                self.table_widget.setItem((i-1), 1, QTableWidgetItem(magnitude))
                self.table_widget.setItem((i-1), 2, QTableWidgetItem(longitude))
                self.table_widget.setItem((i-1), 3, QTableWidgetItem(date))


        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EarthquakeApp()
    window.show()
    sys.exit(app.exec_())
   