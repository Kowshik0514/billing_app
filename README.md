# 🧾 Billing App

A simple desktop application built using **PySide6** and **MySQL** for managing customer bills.

---

## ✨ Features

- Add new customers and generate bills.
- View all customer bills in a neatly styled table.
- Auto-refresh data when new bills are added.
- Responsive UI with light custom styling.
- MySQL database support (via `db.py`).

---

## 🚀 How to Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/Kowshik0514/billing_app.git
   cd billing_app
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

---

## 🛠 Project Structure

```
billing_app/
|
|├— db.py               # Database connection and setup
|├— main.py             # Main application window with tabs
|├— add_bill.py         # UI and logic for adding a new bill
|├— view_data.py        # UI for viewing and displaying bills
|├— requirements.txt    # Python dependencies
└— README.md           # Project documentation
```

---

## ⛁ Database Schema

Tables used:

- **customers** (`id`, `name`, `email`, `phone`)
- **bills** (`id`, `customer_id`, `amount`, `date`)

```sql
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT
);

CREATE TABLE bills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    amount REAL NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);
```

---