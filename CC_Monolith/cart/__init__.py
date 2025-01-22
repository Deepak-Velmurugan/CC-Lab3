from cart import dao
from products import get_product


def get_cart(username: str) -> list:
    cart_contents = dao.get_cart(username)
    return [get_product(product_id) for product_id in cart_contents]


def add_to_cart(username: str, product_id: int):
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int):
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str):
    dao.delete_cart(username)

