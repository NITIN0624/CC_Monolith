from products import dao


class Product:
    def __init__(self, id: int, name: str, description: str, cost: float, qty: int = 0):
        self.id = id
        self.name = name
        self.description = description
        self.cost = cost
        self.qty = qty

    @staticmethod
    def load(data):
        return Product(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            cost=data['cost'],
            qty=data['qty']
        )


def list_products() -> list[Product]:
    """
    Retrieve all products from the database and return as a list of Product objects.
    Optimized for bulk operations.
    """
    # Fetch all products from DAO in a single call
    products = dao.list_products()

    # Use a list comprehension for faster object creation
    return [Product.load(product) for product in products]


def get_product(product_id: int) -> Product:
    """
    Retrieve a single product by ID.
    """
    # Fetch product data and load it into a Product object
    product_data = dao.get_product(product_id)
    if not product_data:
        raise ValueError(f"Product with ID {product_id} not found.")
    return Product.load(product_data)


def add_product(product: dict):
    """
    Add a new product to the database.
    """
    dao.add_product(product)


def update_qty(product_id: int, qty: int):
    """
    Update the quantity of a product. Raise an error if qty is invalid.
    """
    if qty < 0:
        raise ValueError('Quantity cannot be negative')

    # Perform the update directly in the database
    dao.update_qty(product_id, qty)
