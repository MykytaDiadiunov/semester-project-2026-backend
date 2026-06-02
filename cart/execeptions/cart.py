class CartNoItemsError(Exception):
    def __init__(self):
        super().__init__("Cart have no items!")
