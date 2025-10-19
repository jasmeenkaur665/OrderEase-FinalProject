import tkinter as tk
from tkinter import ttk, messagebox

from customer import Customer
from product import Product
from order import Order
from data import MENU, PIZZA_SIZES

class OrderEaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OrderEase - Pizza Ordering System")
        self.root.geometry("750x600")
        self.root.resizable(False, False)

        self.order = None

        # ---------------- Customer Info ----------------
        tk.Label(root, text="Customer Name:", font=("Arial", 12)).place(x=20, y=20)
        self.name_entry = tk.Entry(root, font=("Arial", 12))
        self.name_entry.place(x=160, y=20, width=200)

        tk.Label(root, text="Phone Number:", font=("Arial", 12)).place(x=20, y=60)
        self.phone_entry = tk.Entry(root, font=("Arial", 12))
        self.phone_entry.place(x=160, y=60, width=200)

        self.start_order_button = tk.Button(root, text="Start Order", font=("Arial", 12),
                                            command=self.create_order)
        self.start_order_button.place(x=400, y=40)

        # ---------------- Pizza Selection ----------------
        tk.Label(root, text="Select Size:", font=("Arial", 12)).place(x=20, y=120)
        self.size_combo = ttk.Combobox(root, values=PIZZA_SIZES, state="readonly", font=("Arial", 12))
        self.size_combo.place(x=160, y=120, width=150)
        self.size_combo.bind("<<ComboboxSelected>>", self.update_pizza_types)

        tk.Label(root, text="Select Pizza:", font=("Arial", 12)).place(x=20, y=160)
        self.pizza_combo = ttk.Combobox(root, values=[], state="readonly", font=("Arial", 12))
        self.pizza_combo.place(x=160, y=160, width=150)

        tk.Label(root, text="Quantity:", font=("Arial", 12)).place(x=20, y=200)
        self.qty_entry = tk.Entry(root, font=("Arial", 12))
        self.qty_entry.place(x=160, y=200, width=80)

        self.add_button = tk.Button(root, text="Add to Order", font=("Arial", 12),
                                    command=self.add_to_order)
        self.add_button.place(x=260, y=200)

        # ---------------- Receipt Section ----------------
        tk.Label(root, text="Order Receipt:", font=("Arial", 12, "bold")).place(x=450, y=20)
        self.receipt_box = tk.Text(root, font=("Courier", 11), width=35, height=25, borderwidth=2, relief="solid")
        self.receipt_box.place(x=450, y=60)

        self.finish_button = tk.Button(root, text="Generate Receipt", font=("Arial", 12),
                                       command=self.show_receipt)
        self.finish_button.place(x=480, y=480)

        # ---------------- Step 9: Additional Buttons ----------------
        self.clear_button = tk.Button(root, text="New Order", font=("Arial", 12),
                                      command=self.clear_order)
        self.clear_button.place(x=350, y=480)

        self.save_button = tk.Button(root, text="Save Receipt", font=("Arial", 12),
                                     command=self.save_receipt)
        self.save_button.place(x=450, y=520)

        self.exit_button = tk.Button(root, text="Exit", font=("Arial", 12),
                                     command=self.root.quit)
        self.exit_button.place(x=600, y=520)

    # ---------------- Functions ----------------
    def create_order(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        if not name or not phone:
            messagebox.showerror("Error", "Please enter customer name and phone number")
            return
        self.order = Order(Customer(name, phone))
        self.receipt_box.delete(1.0, tk.END)
        messagebox.showinfo("Order Created", f"Order started for {name}")

    def update_pizza_types(self, event):
        size = self.size_combo.get()
        if size:
            pizzas = list(MENU[size].keys())
            self.pizza_combo['values'] = pizzas

    def add_to_order(self):
        if not self.order:
            messagebox.showerror("Error", "Start an order first!")
            return

        size = self.size_combo.get()
        pizza_name = self.pizza_combo.get()
        qty = self.qty_entry.get()

        if not size or not pizza_name or not qty:
            messagebox.showerror("Error", "Please select size, pizza and quantity")
            return

        try:
            qty = int(qty)
            if qty <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Enter a valid quantity")
            return

        price = MENU[size][pizza_name]
        product = Product(pizza_name, size, price)
        self.order.add_item(product, qty)

        messagebox.showinfo("Added", f"Added {qty} x {size} {pizza_name}")

    def show_receipt(self):
        if not self.order or not self.order.items:
            messagebox.showerror("Error", "No items in the order to show")
            return

        self.receipt_box.delete(1.0, tk.END)
        receipt = self.order.generate_receipt()
        self.receipt_box.insert(tk.END, receipt)

    # ---------------- Step 9.1 & 9.2: Clear, Save, Exit ----------------
    def clear_order(self):
        self.order = None
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.size_combo.set('')
        self.pizza_combo.set('')
        self.qty_entry.delete(0, tk.END)
        self.receipt_box.delete(1.0, tk.END)
        messagebox.showinfo("Reset", "Order cleared successfully!")

    def save_receipt(self):
        if not self.order or not self.order.items:
            messagebox.showerror("Error", "No receipt to save!")
            return

        receipt_data = self.order.generate_receipt()
        with open("receipt.txt", "w") as file:
            file.write(receipt_data)

        messagebox.showinfo("Saved", "Receipt saved as receipt.txt")

def main():
    root = tk.Tk()
    app = OrderEaseApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()