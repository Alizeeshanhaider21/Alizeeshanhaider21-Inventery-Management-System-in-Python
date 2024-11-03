# main.py

import csv
from product import Product
from auth import AuthService

class InventoryManagementSystem:
    PURCHASES_CSV = 'purchases.csv'
 
    def __init__(self, csv_file='inventory.csv'):
        self.products = {}  # Store products by product_id
        self.csv_file = csv_file
        self.auth_service = AuthService()
        self.load_products_from_csv()

    def load_products_from_csv(self):
        """Load products from the CSV file into the products dictionary."""
        try:
            with open(self.csv_file, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    product = Product.from_dict(row)
                    self.products[product.product_id] = product
            print("Products loaded successfully.")
        except FileNotFoundError:
            print("No existing inventory found. Starting with an empty inventory.")

    def save_products_to_csv(self):
        """Save all products from the products dictionary to the CSV file."""
        with open(self.csv_file, mode='w', newline='') as file:
            fieldnames = ["product_id", "name", "category", "price", "stock_quantity","low_stock_threshold"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for product in self.products.values():
                writer.writerow(product.to_dict())
        print("Products saved successfully.")

    def add_product(self, product):
        if product.product_id in self.products:
            print("Product ID already exists.")
        else:
            self.products[product.product_id] = product
            self.save_products_to_csv()
            print("Product added successfully.")

    def delete_product(self, product_id):
        if product_id in self.products:
            del self.products[product_id]
            self.save_products_to_csv()
            print("Product deleted successfully.")
        else:
            print("Product not found.")

    def edit_product(self, product_id, **kwargs):
        product = self.products.get(product_id)
        if product:
            product.edit_product(**kwargs)
            self.save_products_to_csv()
        else:
            print("Product not found.")
   
    def view_inventory(self):
        if not self.products:
            print("The inventory is empty. Please add products to view them here.")
        else:
            for product in self.products.values():
                print(product)
        

    def search_product(self, search_term):
        results = [product for product in self.products.values() if search_term.lower() in product.name.lower()]
        if results:
            for product in results:
                print(product)
        else:
            print("No products found.")

# main.py (excerpt)
    # main.py (excerpt)

    def run(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        user = self.auth_service.authenticate(username, password)
        
        if user:
            print(f"\nWelcome, {username}! You are logged in as a {user.role}.")
            
            while True:
                print("\nChoose an option:")
                
                # Admin menu
                if user.role == "Admin":
                    print("1. Add Product")
                    print("2. Edit Product")
                    print("3. Delete Product")
                    print("4. View Inventory")
                    print("5. Search Product")
                    print("6. Exit")
                    
                    choice = input("Enter choice: ")
                    
                    if choice == "1":
                        product_id = input("Product ID: ")
                        name = input("Product Name: ")
                        category = input("Category: ")
                        price = float(input("Price: "))
                        stock_quantity = int(input("Stock Quantity: "))
                        low_stock_threshold = int(input("Low Stock Threshold: "))  # Prompt for low stock threshold
                        product = Product(product_id, name, category, price, stock_quantity, low_stock_threshold)
                        self.add_product(product)

                    elif choice == "2":
                        product_id = input("Product ID to edit: ")
                        name = input("New name (leave blank to keep current): ")
                        category = input("New category (leave blank to keep current): ")
                        price = input("New price (leave blank to keep current): ")
                        stock_quantity = input("New stock quantity (leave blank to keep current): ")
                        low_stock_threshold = input("New low stock threshold (leave blank to keep current): ")
                        kwargs = {k: v for k, v in [("name", name), ("category", category), ("price", price), 
                                                    ("stock_quantity", stock_quantity), ("low_stock_threshold", low_stock_threshold)] if v}
                        self.edit_product(product_id, **kwargs)

                    elif choice == "3":
                        product_id = input("Product ID to delete: ")
                        self.delete_product(product_id)

                    elif choice == "4":
                        self.view_inventory()

                    elif choice == "5":
                        search_term = input("Search product by name or category: ")
                        self.search_product(search_term)

                    elif choice == "6":
                        print("Exiting system.")
                        break

                    else:
                        print("Invalid choice. Please try again.")

                # User menu
                elif user.role == "User":
                    print("1. View Inventory")
                    print("2. Search Product")
                    print("3. Buy Product")
                    print("4. Exit")

                    choice = input("Enter choice: ")

                    if choice == "1":
                        self.view_inventory()

                    elif choice == "2":
                        search_term = input("Search product by name or category: ")
                        self.search_product(search_term)

                    elif choice == "3":
                        self.buy_product()

                    elif choice == "4":
                        print("Exiting system.")
                        break

                    else:
                        print("Invalid choice. Please try again.")
                        
        else:
            print("Invalid login. Exiting the system.")

    # main.py (excerpt)

    def buy_product(self):
        """Handles the buying process for a user and saves purchase information."""
        product_name = input("Enter the Product Name to buy: ").strip().lower()
        
        # Find product by name (case-insensitive)
        product = next((prod for prod in self.products.values() if prod.name.lower() == product_name), None)
        
        if not product:
            print("Product not found.")
            return
        
        try:
            quantity = int(input(f"Enter quantity to buy (Available: {product.stock_quantity}): "))
            if quantity <= 0:
                print("Quantity should be greater than zero.")
                return
            
            if quantity > product.stock_quantity:
                print("Not enough stock available.")
            else:
                # Gather buyer information
                buyer_name = input("Enter your name: ").strip()
                contact_number = input("Enter your contact number: ").strip()
                
                # Calculate total amount
                total_amount = quantity * product.price
                
                # Update stock and save product changes
                product.update_stock(-quantity)
                self.save_products_to_csv()
                
                # Display purchase summary
                print(f"You bought {quantity} of {product.name}. Total amount: ${total_amount:.2f}")
                print(f"Remaining stock: {product.stock_quantity}")
                
                # Check for low stock based on the custom threshold
                if product.stock_quantity <= product.low_stock_threshold:
                    print(f"Warning: Low stock for {product.name}! Only {product.stock_quantity} left in inventory.")
                
                # Save purchase information to CSV
                self.save_purchase_record(buyer_name, contact_number, product.name, quantity, product.price, total_amount)
        
        except ValueError:
            print("Invalid quantity entered. Please enter a number.")
    
    def save_purchase_record(self, buyer_name, contact_number, product_name, quantity, price_per_unit, total_amount):
            """Save the purchase details in the purchases.csv file."""
            with open(self.PURCHASES_CSV, mode='a', newline='') as file:
                writer = csv.writer(file)
                # Write headers if the file is new/empty
                if file.tell() == 0:
                    writer.writerow(["Buyer Name", "Contact Number", "Product Name", "Quantity", "Price per Unit", "Total Amount"])
                writer.writerow([buyer_name, contact_number, product_name, quantity, price_per_unit, total_amount])
            
            print("Purchase record saved successfully.")
# Run the system if main.py is executed directly
if __name__ == "__main__":
    ims = InventoryManagementSystem()
    ims.run()
