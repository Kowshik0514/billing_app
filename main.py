import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget # type: ignore
from billing_form import BillingForm
from view_data import ViewData

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("💼 Smart Billing App")
        self.setMinimumSize(600, 400)

        tabs = QTabWidget()
        self.view_data_widget = ViewData()
        tabs.addTab(BillingForm(view_data_widget=self.view_data_widget), "📝 Add Bill")
        tabs.addTab(self.view_data_widget, "📄 View Records")

        self.setCentralWidget(tabs)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
