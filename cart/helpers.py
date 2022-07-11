from core.models import Cart


class CartHelper:
    def __init__(self, user):
        self.user = user
        self.cart_items = []
        self.cart_total_price = 0

    def calculate_cart_price(self):
        self.cart_items = Cart.objects.filter(user=self.user)
        if not self.cart_items:
            return False

        for cart_item in self.cart_items:
            self.cart_total_price += cart_item.product.price * \
                                     cart_item.quantity
        return self.cart_total_price
