# product.py

class Product:
    def __init__(self, product_id, name, category, price, stock_quantity, low_stock_threshold):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock_quantity = stock_quantity
        self.low_stock_threshold = low_stock_threshold  # New attribute for low stock threshold

    def update_stock(self, quantity):
        self.stock_quantity += quantity
        print(f"Stock updated! New quantity: {self.stock_quantity}")

    def edit_product(self, name=None, category=None, price=None, stock_quantity=None, low_stock_threshold=None):
        if name:
            self.name = name
        if category:
            self.category = category
        if price:
            self.price = price
        if stock_quantity:
            self.stock_quantity = stock_quantity
        if low_stock_threshold:
            self.low_stock_threshold = low_stock_threshold
        print(f"Product {self.product_id} updated.")

    def to_dict(self):
        """Convert product data to a dictionary for CSV storage."""
        return {
            "product_id": self.product_id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "stock_quantity": self.stock_quantity,
            "low_stock_threshold": self.low_stock_threshold  # Include low stock threshold in CSV data
        }

    @staticmethod
    def from_dict(data):
        """Create a Product instance from a dictionary."""
        return Product(
            product_id=data["product_id"],
            name=data["name"],
            category=data["category"],
            price=float(data["price"]),
            stock_quantity=int(data["stock_quantity"]),
            low_stock_threshold=int(data["low_stock_threshold"])  # Parse low stock threshold from CSV
        )

    def __str__(self):
        """Define how the product is displayed as a string."""
        return (f"ID: {self.product_id}, Name: {self.name}, Category: {self.category}, "
                f"Price: {self.price}, Stock: {self.stock_quantity}, "
                f"Low Stock Threshold: {self.low_stock_threshold}")
