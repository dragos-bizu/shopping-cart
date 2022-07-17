from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from cart.tests.test_cart_api import CART_CHECKOUT_URL
from cart.tests.utils import create_sample_product, \
    create_sample_product_size, \
    create_sample_cart, create_sample_user_profile
from core.models import Order, OrderItems, OrderItemStatus
from order.tests.utils import create_sample_order, create_sample_order_item

ORDER_RETURN_URL = reverse('order_return')


class OrderApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test", password="password"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_checkout_create_order(self):
        """Test checkout create order"""

        my_product_1 = create_sample_product('Pajamas')
        my_product_size_1 = create_sample_product_size(my_product_1, 'XL', 1)
        my_product_2 = create_sample_product('Skirt')
        my_product_size_2 = create_sample_product_size(my_product_2, 'M', 2)

        create_sample_user_profile(self.user)

        create_sample_cart(self.user, my_product_1,
                           my_product_size_1, 1)
        create_sample_cart(self.user, my_product_2,
                           my_product_size_2, 2)

        self.client.post(CART_CHECKOUT_URL)

        exists = Order.objects.filter(user=self.user).exists()

        self.assertTrue(exists)

    def test_checkout_create_order_items(self):
        """Test checkout create order items"""

        my_product_1 = create_sample_product('Jacket')
        my_product_size_1 = create_sample_product_size(my_product_1, 'XL', 1)
        my_product_2 = create_sample_product('Coat')
        my_product_size_2 = create_sample_product_size(my_product_2, 'M', 2)

        create_sample_user_profile(self.user)

        create_sample_cart(self.user, my_product_1,
                           my_product_size_1, 1)
        create_sample_cart(self.user, my_product_2,
                           my_product_size_2, 2)

        self.client.post(CART_CHECKOUT_URL)

        order = Order.objects.get(user=self.user)
        order_items = OrderItems.objects.filter(order=order)

        self.assertEqual(order_items[0].product, my_product_1)
        self.assertEqual(order_items[0].product_size, my_product_size_1)
        self.assertEqual(order_items[1].product, my_product_2)
        self.assertEqual(order_items[1].product_size, my_product_size_2)

    def test_order_return(self):
        my_product_1 = create_sample_product('Tracksuit')
        my_product_size_1 = create_sample_product_size(my_product_1, 'XL', 1)

        create_sample_user_profile(self.user)

        order = create_sample_order(self.user)
        my_order_item_1 = create_sample_order_item(order, my_product_1,
                                                   my_product_size_1, 1)

        payload = {'order_item_id': my_order_item_1.id}
        self.client.post(ORDER_RETURN_URL, payload)

        my_order_item_1 = OrderItems.objects.get(order=order)

        self.assertEqual(my_order_item_1.status, OrderItemStatus.returned)
