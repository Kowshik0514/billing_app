from PySide6.QtWidgets import QWidget, QLineEdit, QPushButton, QFormLayout, QVBoxLayout, QMessageBox, QGroupBox # type: ignore
from db import get_connection
from datetime import datetime

class BillingForm(QWidget):
    def __init__(self, view_data_widget):
        super().__init__()

        self.setStyleSheet("""
            QLabel { font-size: 14px; }
            QLineEdit { padding: 6px; font-size: 14px; border-radius: 4px; border: 1px solid #ccc; }
            QPushButton {
                padding: 8px 16px; background-color: #0078D7; color: white;
                font-weight: bold; border-radius: 6px;
            }
            QPushButton:hover { background-color: #005BBB; }
        """)

        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.amount_input = QLineEdit()

        form_layout = QFormLayout()
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Phone:", self.phone_input)
        form_layout.addRow("Amount (₹):", self.amount_input)

        group_box = QGroupBox("Enter Billing Details")
        group_box.setLayout(form_layout)

        self.submit_button = QPushButton("💾 Submit")
        self.submit_button.clicked.connect(self.save_data)

        self.view_data_widget = view_data_widget
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(group_box)
        main_layout.addWidget(self.submit_button)
        self.setLayout(main_layout)

    def save_data(self):
        name = self.name_input.text()
        email = self.email_input.text()
        phone = self.phone_input.text()
        amount = self.amount_input.text()

        if not all([name, email, phone, amount]):
            QMessageBox.warning(self, "Missing Info", "Please fill all fields.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO customers (name, email, phone) VALUES (%s, %s, %s)",
                       (name, email, phone))
        customer_id = cursor.lastrowid
        cursor.execute("INSERT INTO bills (customer_id, amount, date) VALUES (%s, %s, %s)",
                       (customer_id, amount, datetime.now()))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Saved", "Billing info saved successfully!")
        self.view_data_widget.load_data()
        
        self.name_input.clear()
        self.email_input.clear()
        self.phone_input.clear()
        self.amount_input.clear()
