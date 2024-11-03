# product.py

class Product:
    def __init__(self, product_id, name, category, price, stock_quantity):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock_quantity = stock_quantity
   
    def update_stock(self, quantity):
        self.stock_quantity += quantity
        print(f"Stock updated! New quantity: {self.stock_quantity}")

    def edit_product(self, name=None, category=None, price=None, stock_quantity=None):
        if name:
            self.name = name
        if category:
            self.category = category
        if price:
            self.price = price
        if stock_quantity:
            self.stock_quantity = stock_quantity
        print(f"Product {self.product_id} updated.")

    def to_dict(self):
        """Convert product data to a dictionary for CSV storage."""
        return {
            "product_id": self.product_id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "stock_quantity": self.stock_quantity
        }
    
    @staticmethod
    def from_dict(data):
        """Create a Product instance from a dictionary."""
        return Product(
            product_id=data["product_id"],
            name=data["name"],
            category=data["category"],
            price=float(data["price"]),
            stock_quantity=int(data["stock_quantity"])
        )

    def __str__(self):
        return f"ID: {self.product_id}, Name: {self.name}, Category: {self.category}, Price: {self.price}, Stock: {self.stock_quantity}"
