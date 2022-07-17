from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from django.contrib.auth import get_user_model
from django.urls import reverse

from cart.helpers import CartHelper
from cart.tests.utils import create_sample_product, \
    create_sample_product_size, \
    create_sample_cart, create_sample_user_profile
from core.models import Cart, UserProfile

CART_ADD_URL = reverse('cart_add')
CART_DETAILS_URL = reverse('cart_details')
CART_CHECKOUT_URL = reverse('cart_checkout')


class CartApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test", password="password"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_add_product_succesfully(self):
        """Test add a product to cart"""
        my_product = create_sample_product('Jeans')
        my_product_size = create_sample_product_size(my_product, 'XL', 2)
        payload = {'product': my_product.id,
                   'product_size': my_product_size.id,
                   'quantity': 1}
        self.client.post(CART_ADD_URL, payload)

        exists = Cart.objects.filter(user=self.user,
                                     product=my_product).exists()

        self.assertTrue(exists)

    def test_add_product_out_of_stock(self):
        """Test add product out of stock to cart"""
        my_product = create_sample_product('Jeans')
        my_product_size = create_sample_product_size(my_product, 'XL', 0)
        payload = {'product': my_product.id,
                   'product_size': my_product_size.id,
                   'quantity': 1}
        res = self.client.post(CART_ADD_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_calculate_total_price_cart(self):
        """Test calculate total price for cart products"""
        my_product_1 = create_sample_product('Jeans')
        my_product_size_1 = create_sample_product_size(my_product_1, 'XL', 1)
        my_product_2 = create_sample_product('T-Shirt')
        my_product_size_2 = create_sample_product_size(my_product_2, 'M', 2)

        create_sample_cart(self.user, my_product_1,
                           my_product_size_1, 1)
        create_sample_cart(self.user, my_product_2,
                           my_product_size_2, 2)
        cart_helper = CartHelper(self.user)
        cart_total_price = cart_helper.calculate_cart_price()

        self.assertEqual(cart_total_price, 60.00)

    def test_cart_checkout(self):
        """Test cart checkout"""
        my_product_1 = create_sample_product('Vest')
        my_product_size_1 = create_sample_product_size(my_product_1, 'XL', 1)
        my_product_2 = create_sample_product('Sweater')
        my_product_size_2 = create_sample_product_size(my_product_2, 'M', 2)

        create_sample_user_profile(self.user)

        create_sample_cart(self.user, my_product_1,
                           my_product_size_1, 1)
        create_sample_cart(self.user, my_product_2,
                           my_product_size_2, 2)

        res = self.client.post(CART_CHECKOUT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_cart_checkout_update_wallet(self):
        """Test cart checkout update wallet"""
        my_product_1 = create_sample_product('Pajamas')
        my_product_size_1 = create_sample_product_size(my_product_1, 'XL', 1)
        my_product_2 = create_sample_product('Socks')
        my_product_size_2 = create_sample_product_size(my_product_2, 'M', 2)

        create_sample_user_profile(self.user)

        create_sample_cart(self.user, my_product_1,
                           my_product_size_1, 1)
        create_sample_cart(self.user, my_product_2,
                           my_product_size_2, 2)

        self.client.post(CART_CHECKOUT_URL)

        my_user_profile = UserProfile.objects.get(user=self.user)

        self.assertEqual(my_user_profile.wallet, 1000-60)


    def test_cart_checkout_not_enough_money(self):
        """Test cart checkout not enough money in wallet"""
        my_product_1 = create_sample_product('Jeans')
        my_product_size_1 = create_sample_product_size(my_product_1, 'XL', 1)
        my_product_2 = create_sample_product('Jacket')
        my_product_size_2 = create_sample_product_size(my_product_2, 'M', 2)

        create_sample_user_profile(self.user, wallet=10)

        create_sample_cart(self.user, my_product_1,
                           my_product_size_1, 1)
        create_sample_cart(self.user, my_product_2,
                           my_product_size_2, 2)

        res = self.client.post(CART_CHECKOUT_URL)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
