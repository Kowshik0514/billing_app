import csv
from PySide6.QtWidgets import ( # type: ignore
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QLineEdit, QPushButton, QHBoxLayout, QFileDialog
)
from PySide6.QtGui import QFont, QColor, QBrush # type: ignore
from PySide6.QtCore import Qt # type: ignore
from db import get_connection


class ViewData(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e1e;
                color: #f0f0f0;
                border: 1px solid #444;
                gridline-color: #555;
                font-size: 14px;
                border-radius: 8px;
            }

            QHeaderView::section {
                background-color: #333;
                color: #fff;
                padding: 8px;
                border: 1px solid #444;
                font-weight: bold;
            }

            QLineEdit {
                padding: 6px;
                font-size: 14px;
                border: 1px solid #555;
                border-radius: 6px;
                color: white;
                background-color: #2e2e2e;
            }

            QPushButton {
                padding: 6px 14px;
                background-color: #0078D7;
                color: white;
                font-weight: bold;
                border-radius: 6px;
            }

            QPushButton:hover {
                background-color: #005BBB;
            }
        """)

        layout = QVBoxLayout()

        header_label = QLabel("📄 Customer Bills")
        header_label.setFont(QFont("Arial", 16, QFont.Bold))
        header_label.setStyleSheet("color: white; padding: 8px;")
        layout.addWidget(header_label)

        search_export_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by Name, Email or Phone...")
        self.search_input.textChanged.connect(self.filter_data)

        export_button = QPushButton("📤 Export CSV")
        export_button.clicked.connect(self.export_csv)

        search_export_layout.addWidget(self.search_input)
        search_export_layout.addWidget(export_button)
        layout.addLayout(search_export_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["👤 Name", "📧 Email", "📞 Phone", "💰 Amount", "📅 Date"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)

        layout.addWidget(self.table)
        self.setLayout(layout)

        self.all_data = []
        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.name, c.email, c.phone, b.amount, b.date
            FROM customers c JOIN bills b ON c.id = b.customer_id
            ORDER BY b.date DESC
        """)
        self.all_data = cursor.fetchall()
        conn.close()
        self.populate_table(self.all_data)

    def populate_table(self, data):
        self.table.setRowCount(0)
        for row_index, row in enumerate(data):
            self.table.insertRow(row_index)
            for col_index, value in enumerate(row):
                item = QTableWidgetItem(str(value if value else "N/A"))
                item.setTextAlignment(Qt.AlignCenter)
                item.setFont(QFont("Segoe UI", 12))
                item.setForeground(QBrush(QColor("#ffffff")))
                self.table.setItem(row_index, col_index, item)

    def filter_data(self):
        query = self.search_input.text().lower()
        filtered = [row for row in self.all_data if query in str(row[0]).lower() or query in str(row[1]).lower() or query in str(row[2]).lower()]
        self.populate_table(filtered)

    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "bills.csv", "CSV Files (*.csv)")
        if path:
            with open(path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Email", "Phone", "Amount", "Date"])
                for row_index in range(self.table.rowCount()):
                    row_data = [
                        self.table.item(row_index, col).text()
                        for col in range(self.table.columnCount())
                    ]
                    writer.writerow(row_data)
