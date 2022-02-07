import sys

from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm

from rest_framework import status

from diplom.models import User, Contact, Shop, ProductInfo, Order
from django.urls import path, reverse

from diplom.views import PartnerUpdate, RegisterAccount, LoginAccount, CategoryView, ShopView, ProductInfoView, \
    BasketView, \
    AccountDetails, ContactView, OrderView, PartnerState, PartnerOrders, ConfirmAccount
from rest_framework.test import APITestCase, URLPatternsTestCase, APIRequestFactory, force_authenticate

factory = APIRequestFactory()


class TestPartner(APITestCase, URLPatternsTestCase, APIRequestFactory):
    urlpatterns = [

        path('user/login', LoginAccount.as_view(), name='user-login'),
        path('partner/state', PartnerState.as_view(), name='partner-state'),
        path('partner/orders', PartnerOrders.as_view(), name='partner-orders'),
    ]

    @classmethod
    def setUpTestData(cls):
        "Создаем пользователя, контакт и магазин для дальнейшего использования."
        User.objects.create_user(first_name='Pavel', last_name='Shatilov', email='real@gmail.com',
                                 password='789', company='Bulki', position='Manager', is_active=True, type='shop')
        user = User.objects.first()
        c = Contact(user=user, city='Chernihiv', street='Shevchenko 32', house='134', structure='1',
                    building='1', apartment='1', phone='776588566')
        c.save()
        shop = Shop(name='Связной', user=user, state=True)
        shop.save()

    def test_login_account(self):
        "Проверка авторизации польхователя по API"
        # 'user/login'

        user = User.objects.get(id=1)
        url = reverse('user-login')
        data = {'email': 'real@gmail.com', 'password': '789'}
        response = self.client.post(url, data)
        token_key = response.json().get('Token')

        self.assertEqual(user.is_active, True)
        self.assertEqual(response.json().get('Status'), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return token_key

    def test_status_partner(self):
        "Поулчение статуса маназина по API"
        # 'partner/state'

        token_key = self.test_login_account()
        url = reverse('partner-state')
        response = self.client.get(url, HTTP_AUTHORIZATION='Token ' + token_key)
        self.assertEqual(response.json().get('name'), 'Связной')
        self.assertEqual(response.json().get('state'), True)

    def test_change_status_partner(self):
        "Проверка изменения статуса партнера по API"
        # 'partner/state'

        token_key = self.test_login_account()
        url = reverse('partner-state')
        data = {'state': 'off'}
        response = self.client.post(url, data=data, HTTP_AUTHORIZATION='Token ' + token_key)
        self.assertEqual(response.json().get('Status'), True)

        response = self.client.get(url, HTTP_AUTHORIZATION='Token ' + token_key)
        self.assertEqual(response.json().get('state'), False)

        data1 = {'state': 'on'}
        response = self.client.post(url, data=data1, HTTP_AUTHORIZATION='Token ' + token_key)
        self.assertEqual(response.json().get('Status'), True)

        response = self.client.get(url, HTTP_AUTHORIZATION='Token ' + token_key)
        self.assertEqual(response.json().get('state'), True)

    def test_get_orders(self):
        "Проверка получения заказов по партнеру"
        # 'partner/orders'

        token_key = self.test_login_account()
        url = reverse('partner-orders')
        response = self.client.get(url, HTTP_AUTHORIZATION='Token ' + token_key)

        self.assertEqual(response.json(), [])


class TestUsers(APITestCase, URLPatternsTestCase, APIRequestFactory):
    urlpatterns = [

        path('user/register', RegisterAccount.as_view(), name='user-register'),
        path('user/details', AccountDetails.as_view(), name='user-details'),
        path('user/contact', ContactView.as_view(), name='user-contact'),
        path('user/login', LoginAccount.as_view(), name='user-login'),

    ]

    @classmethod
    def setUpTestData(cls):
        "Создаем пользователя, контакт и магазин для дальнейшего использования."
        User.objects.create_user(first_name='Pavel', last_name='Shatilov', email='real@gmail.com',
                                 password='789', company='Bulki', position='Manager', is_active=True, type='shop')
        user = User.objects.first()
        c = Contact(user=user, city='Chernihiv', street='Shevchenko 32', house='134', structure='1',
                    building='1', apartment='1', phone='776588566')
        c.save()
        shop = Shop(name='Связной', user=user, state=True)
        shop.save()

    def test_create_user_db(self):
        "Проверка успешности создания пользователя, контакта, магазина."

        user = User.objects.first()
        self.assertEquals(user.company, 'Bulki')

        contact = Contact.objects.first()
        self.assertEquals(contact.city, 'Chernihiv')

        shop = Shop.objects.first()
        self.assertEquals(shop.name, 'Связной')

    def test_create_account(self):
        "Проверка регистрации пользователя по API"
        # 'user/register'

        url = reverse('user-register')
        data = {'first_name': 'Pavel', 'last_name': 'Shatilov', 'email': 'real1@gmail.com', 'password': 'Shatilov789',
                'company': 'Bulki', 'position': 'Manager'}

        response = self.client.post(url, data)
        self.assertEqual(response.json().get('Status'), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_account(self):
        "Проверка авторизации польхователя по API"
        # 'user/login'

        user = User.objects.first()
        url = reverse('user-login')
        data = {'email': 'real@gmail.com', 'password': '789'}
        response = self.client.post(url, data)
        token_key = response.json().get('Token')

        self.assertEqual(user.is_active, True)
        self.assertEqual(response.json().get('Status'), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return token_key

    def test_create(self):
        "Создание контакта по API"
        # 'user/contact'

        token_key = self.test_login_account()
        url = reverse('user-contact')
        data = {'city': 'Chernihiv', 'street': 'Shevchenko 32', 'house': '134', 'structure': '1',
                'building': '1', 'apartment': '1', 'phone': '776588566'}
        response = self.client.post(url, HTTP_AUTHORIZATION='Token ' + token_key, data=data, verify=False)

        self.assertEqual(response.json().get('Status'), True)

    def test_update_contact(self):
        "Проверка изменения контакта по API"
        # 'user/contact'

        contact = Contact.objects.first()
        token_key = self.test_login_account()
        url = reverse('user-contact')

        self.assertEqual(contact.city, "Chernihiv")
        self.assertEqual(contact.id, 3)

        data1 = {'city': 'Korukivka', 'street': 'Pro 32', 'house': '32', 'structure': '2',
                 'building': '2', 'apartment': '2', 'phone': '4364366', 'id': '3'}
        response = self.client.put(url, data=data1, HTTP_AUTHORIZATION='Token ' + token_key)
        cont = Contact.objects.first()

        self.assertEqual(response.json().get('Status'), True)
        self.assertEqual(cont.city, "Korukivka")

    def test_edit_user(self):
        "Проверка редоктирвоания пользрвателя по API"
        # 'user/details'

        token_key = self.test_login_account()
        url = reverse('user-details')
        data = {'first_name': 'Vova', 'last_name': 'Shatilov', 'email': 'borsh1@gmail.com',
                'password': 'BobShnauder789',
                'company': 'Pirozki', 'position': 'Director', 'id': '1'}
        response = self.client.post(url, data=data, HTTP_AUTHORIZATION='Token ' + token_key)
        user = User.objects.first()
        self.assertEqual(response.json().get('Status'), True)
        self.assertEqual(user.first_name, 'Vova')


class TestShop(APITestCase, URLPatternsTestCase, APIRequestFactory):
    urlpatterns = [

        path('user/login', LoginAccount.as_view(), name='user-login'),
        path('partner/update', PartnerUpdate.as_view(), name='partner-update'),
        path('basket', BasketView.as_view(), name='basket'),
        path('products', ProductInfoView.as_view(), name='products'),
        path('shops', ShopView.as_view(), name='shops'),
        path('order', OrderView.as_view(), name='order'),
        path('categories', CategoryView.as_view(), name='categories'),

    ]

    @classmethod
    def setUpTestData(cls):
        "Создаем пользователя, контакт и магазин для дальнейшего использования."
        User.objects.create_user(first_name='Pavel', last_name='Shatilov', email='real@gmail.com',
                                 password='789', company='Bulki', position='Manager', is_active=True, type='shop')
        user = User.objects.first()
        c = Contact(user=user, city='Chernihiv', street='Shevchenko 32', house='134', structure='1',
                    building='1', apartment='1', phone='776588566')
        c.save()
        shop = Shop(name='Связной', user=user, state=True)
        shop.save()

    def test_login_account(self):
        "Проверка авторизации пользователя по API"
        # 'user/login'

        user = User.objects.first()
        url = reverse('user-login')
        data = {'email': 'real@gmail.com', 'password': '789'}
        response = self.client.post(url, data)
        token_key = response.json().get('Token')

        self.assertEqual(user.is_active, True)
        self.assertEqual(response.json().get('Status'), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return token_key

    def test_get_shops(self):
        "Получения списка маганзинов"
        # shops & partner/update

        token_key = self.test_login_account()
        url = reverse('partner-update')
        data = {'url': 'https://raw.githubusercontent.com/netology-code/pd-diplom/master/data/shop1.yaml'}
        response = self.client.post(url, data=data, HTTP_AUTHORIZATION='Token ' + token_key)

        self.assertEqual(response.json().get('Status'), True)

        url = reverse('shops')

        response = self.client.get(url)

        self.assertEqual(response.json()[0].get('name'), 'Связной')

    def test_get_products(self):
        "Получение товаров"
        # products & partner/update

        token_key = self.test_login_account()
        url = reverse('partner-update')
        data = {'url': 'https://raw.githubusercontent.com/netology-code/pd-diplom/master/data/shop1.yaml'}
        response = self.client.post(url, data=data, HTTP_AUTHORIZATION='Token ' + token_key)

        self.assertEqual(response.json().get('Status'), True)

        url = reverse('products')
        data = {"shop_id": 2, "category_id": 224}
        response = self.client.get(url, data=data)

        self.assertEqual(response.json()[0].get('shop'), 2)

    def test_get_product(self):
        "Проверка создание продуктов, получение, добавление, редактирование и удаление продуктов в корзине."
        # 'basket'

        token_key = self.test_login_account()
        url = reverse('partner-update')
        data = {'url': 'https://raw.githubusercontent.com/netology-code/pd-diplom/master/data/shop1.yaml'}
        response = self.client.post(url, data=data, HTTP_AUTHORIZATION='Token ' + token_key)

        self.assertEqual(response.json().get('Status'), True)

        url = reverse('basket')
        data = {"items": '[{"product_info": "1", "quantity": "13"}, {"product_info": 2, "quantity": 12 }]'}
        response = self.client.post(url, data=data, HTTP_AUTHORIZATION='Token ' + token_key)

        self.assertEqual(response.json().get('Создано объектов'), 2)

        url = reverse('basket')
        response = self.client.get(url, HTTP_AUTHORIZATION='Token ' + token_key)
        self.assertEqual(response.json()[0].get('id'), 1)

        url = reverse('basket')
        data = {"items": '[{"id": 1, "quantity": 2 }, { "id": 2, "quantity": 1}]'}
        response = self.client.put(url, data=data, HTTP_AUTHORIZATION='Token ' + token_key)

        self.assertEqual(response.json().get('Обновлено объектов'), 2)

        url = reverse('basket')
        data = {"items": '2'}
        response = self.client.delete(url, data=data, HTTP_AUTHORIZATION='Token ' + token_key)

        self.assertEqual(response.json().get('Удалено объектов'), 1)

        "Проверка привязки контакта к заказу и поулчение заказа"
        url = reverse('order')
        data = {"id": 1, "contact": 2}
        response = self.client.post(url, data=data, HTTP_AUTHORIZATION='Token ' + token_key)
        self.assertEqual(response.json().get('Status'), True)

        url = reverse('order')
        response = self.client.get(url,  HTTP_AUTHORIZATION='Token ' + token_key)
        self.assertEqual(response.json()[0].get('id'), 1)

        "Получение категорий"
        url = reverse('categories')
        response = self.client.get(url,  HTTP_AUTHORIZATION='Token ' + token_key)
        self.assertEqual(response.json().get('count'), 3)