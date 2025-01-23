import json

import products
from cart import dao
from products import Product


class Cart:
    def __init__(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data):
        return Cart(
            id=data['id'],
            username=data['username'],
            contents=[Product(**item) for item in data['contents']],
            cost=data['cost']
        )


def get_cart(username: str) -> list:
    """
    Fetch the cart for a user, optimize product fetching, and return product list.
    """

    # Fetch cart details from the database in a single query
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    # Deserialize JSON contents and collect all product IDs
    all_product_ids = set()  # Use a set to remove duplicates
    try:
        for cart_detail in cart_details:
            contents = json.loads(cart_detail['contents'])  # Use json.loads for safety and speed
            all_product_ids.update(contents)
    except json.JSONDecodeError:
        pass

    if not all_product_ids:
        return []

    # Fetch all products in bulk
    products_map = products.get_products_bulk(list(all_product_ids))  # Bulk fetch all products

    # Build and return the product list in the same order as the cart
    return [products_map[pid] for cart_detail in cart_details for pid in json.loads(cart_detail['contents']) if pid in products_map]


def add_to_cart(username: str, product_id: int):
    """
    Add a product to the user's cart.
    """
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int):
    """
    Remove a product from the user's cart.
    """
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str):
    """
    Delete the user's cart entirely.
    """
    dao.delete_cart(username)
