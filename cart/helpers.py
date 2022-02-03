from .models import Cart


class CartHelper:

    def __init__(self, user):
        self.user = user

        self.cart_items = 0
        self.cart_total_amount = 0
        self.checkout_details = {
            'products': [],
            'total_amount': [],
        }

    def prepare_cart_for_checkout(self):
        self.cart_items = Cart.objects.filter(user=self.user)

        if not self.cart_items:
            return False

        self.calculate_cart_total_amount()
        self.prepare_checkout_details()

        return self.checkout_details

    def calculate_cart_total_amount(self):
        for cart_item in self.cart_items:
            self.cart_total_amount += cart_item.item.price * cart_item.quantity

    def prepare_checkout_details(self):
        for cart_item in self.cart_items:
            self.checkout_details['products'].append(
                {
                    'category_id': cart_item.item.category.id,
                    'category_name': cart_item.item.category.name,
                    'product_id': cart_item.item.id,
                    'product_name': cart_item.item.name,
                    'quantity': cart_item.quantity,
                    'unit_price': cart_item.item.price,
                }
            )
        self.checkout_details['total_amount'].append(
            {
                'total_amount': self.cart_total_amount
            }
        )
