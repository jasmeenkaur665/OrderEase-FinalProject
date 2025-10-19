from datetime import datetime

class Order:
    def __init__(self, customer):
        self.customer = customer    # Customer object
        self.items = []             # List to store (Product, quantity)
        self.timestamp = datetime.now()  # Time of order

    def add_item(self, product, quantity):
        self.items.append((product, quantity))

    def calculate_total(self):
        return sum(product.price * qty for product, qty in self.items)

    def generate_receipt(self):
        receipt = f"----- Order Receipt -----\n"
        receipt += f"Customer: {self.customer.name} ({self.customer.phone})\n"
        receipt += f"Date: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
        receipt += "-------------------------\n"

        for product, qty in self.items:
            line_total = product.price * qty
            receipt += f"{product.size} {product.name} x{qty} = ${line_total:.2f}\n"

        receipt += "-------------------------\n"
        receipt += f"Total Amount: ${self.calculate_total():.2f}\n"
        receipt += "-------------------------\n"

        return receipt