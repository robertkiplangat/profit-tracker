# niko na shida na json
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QHBoxLayout, QComboBox, QTextEdit, QMessageBox,
                             QDateEdit)
import datetime
from PyQt5.QtCore import QDate
import json


class ProfitTrackerApp(QWidget): # hapa ndio code yetu ina anzia
    def __init__(self):
        super().__init__()
        self.initUI()
        self.transactions = []

    def initUI(self):
        self.setWindowTitle("Profit Tracker")
        self.setGeometry(100, 100, 800, 600)

        
        self.item_name_label = QLabel("Item Name:", self)
        self.item_name_input = QLineEdit(self)

        self.buying_price_label = QLabel("Buying Price:", self)
        self.buying_price_input = QLineEdit(self)

        self.marked_price_label = QLabel("Marked Price:", self)
        self.marked_price_input = QLineEdit(self)

        self.discount_label = QLabel("Discount:", self)
        self.discount_input = QLineEdit(self)

        self.quantity_label = QLabel("Quantity Sold:", self)
        self.quantity_input = QLineEdit(self)

        self.start_date_label = QLabel("Start Date:", self)
        self.start_date_input = QDateEdit(self)
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setDate(QDate.currentDate())

        self.end_date_label = QLabel("End Date:", self)
        self.end_date_input = QDateEdit(self)
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.setDate(QDate.currentDate())

        # hizi ni ma buttns tu
        self.record_button = QPushButton("Record Transaction", self)
        self.record_button.clicked.connect(self.record_transaction)

        self.view_button = QPushButton("View Transactions", self)
        self.view_button.clicked.connect(self.view_transactions)

        self.calculate_profit_button = QPushButton("Calculate Total Profit", self)
        self.calculate_profit_button.clicked.connect(self.calculate_total_profit)

        self.calculate_profit_period_button = QPushButton("Calculate Profit by Period", self)
        self.calculate_profit_period_button.clicked.connect(self.calculate_total_profit_by_time_period)

        self.product_name_label = QLabel("Product Name to Calculate Profit:", self)
        self.product_name_input = QLineEdit(self)

        self.calculate_product_profit_button = QPushButton("Calculate Product Profit", self)
        self.calculate_product_profit_button.clicked.connect(self.calculate_product_profit)

        self.output_area = QTextEdit(self)
        self.output_area.setReadOnly(True)

        input_layout = QVBoxLayout()
        input_layout.addWidget(self.item_name_label)
        input_layout.addWidget(self.item_name_input)
        input_layout.addWidget(self.buying_price_label)
        input_layout.addWidget(self.buying_price_input)
        input_layout.addWidget(self.marked_price_label)
        input_layout.addWidget(self.marked_price_input)
        input_layout.addWidget(self.discount_label)
        input_layout.addWidget(self.discount_input)
        input_layout.addWidget(self.quantity_label)
        input_layout.addWidget(self.quantity_input)
        input_layout.addWidget(self.record_button)
        input_layout.addWidget(self.view_button)
        input_layout.addWidget(self.calculate_profit_button)
        input_layout.addWidget(self.start_date_label)
        input_layout.addWidget(self.start_date_input)
        input_layout.addWidget(self.end_date_label)
        input_layout.addWidget(self.end_date_input)
        input_layout.addWidget(self.calculate_profit_period_button)
        input_layout.addWidget(self.product_name_label)
        input_layout.addWidget(self.product_name_input)
        input_layout.addWidget(self.calculate_product_profit_button)

        main_layout = QHBoxLayout()
        main_layout.addLayout(input_layout)  # input side ya left
        main_layout.addWidget(self.output_area)  # input side ya right

        self.setLayout(main_layout)

    def write_transaction_to_file(self, transaction):
        try:
            try:
                with open('transactions.json', 'r') as file:
                    transactions = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                transactions = []

            transactions.append(transaction)

            with open('transactions.json', 'w') as file:
                json.dump(transactions, file, indent=4)

            self.output_area.append(f"Transaction recorded for {transaction['item_name']}!")

        except Exception as e:
            QMessageBox.warning(self, "File Error", f"Error writing to file: {str(e)}")

    def read_transactions_from_file(self):
        try:
            with open('transactions.json', 'r') as file:
                transactions = json.load(file)
        except FileNotFoundError:
            QMessageBox.warning(self, "File Error", "No transactions file found.")
            transactions = []
        except json.JSONDecodeError:
            QMessageBox.warning(self, "File Error", "File is not properly formatted.")
            transactions = []
        except Exception as e:
            QMessageBox.warning(self, "File Error", f"Error reading from file: {str(e)}")
            transactions = []

        return transactions

    def view_transactions(self):
        self.output_area.clear()

        transactions = self.read_transactions_from_file()

        if not transactions:
            self.output_area.append("No transactions recorded yet.")
            return

        self.output_area.append("Transactions:\n")
        for transaction in transactions:
            self.output_area.append(f"Date: {transaction['date']}\n"
                                    f"Item: {transaction['item_name']}\n"
                                    f"Buying Price: {transaction['buying_price']}\n"
                                    f"Marked Price: {transaction['marked_price']}\n"
                                    f"Selling Price: {transaction['selling_price']}\n"
                                    f"Quantity: {transaction['quantity']}\n"
                                    f"Total Profit: {transaction['total_profit']}\n"
                                    f"Profit per Item: {transaction['profit_per_item']}\n")
            self.output_area.append("-" * 40)

    def calculate_total_profit(self):
        self.output_area.clear()
        total_profit = 0

        for transaction in self.transactions:
            total_profit += transaction['total_profit']

        file_transactions = self.read_transactions_from_file()
        for transaction in file_transactions:
            total_profit += transaction['total_profit']

        self.output_area.append(f"Total profit: {total_profit}")
        return total_profit

    def calculate_total_profit_by_time_period(self): 
        pass
    def calculate_product_profit(self): # hii itakuwa ya each indvidual product
       pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ProfitTrackerApp()
    ex.show()
    sys.exit(app.exec_())
