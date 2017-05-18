from decimal import Decimal
from django.conf import settings#载入设置文件
from food.models import Food

class Cart(object):
    def __init__(self, request, table_no=None, message=None):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.table_no = table_no
        self.message = message

    def add(self, food, quantity=1, update_quantity=False):
        food_id = str(food.id)
        if food_id not in self.cart:
            self.cart[food_id] = {'quantity': quantity, 'price': str(food.price)}
        if update_quantity:
            self.cart[food_id]['quantity'] = quantity
        else:
            self.cart[food_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, food):
        food_id = food.id
        if food_id in self.cart:
            del self.cart[food_id]
            self.save()

    #迭代魔术方法，使得购物车可以被作用与循环语句
    #这是使得购物车实例对象可以被作用于循环语句而不是之前的纯粹是字典被作用于循环语句
    def __iter__(self):
        food_ids = self.cart.keys()
        foods = Food.objects.filter(id__in=food_ids)
        for food in foods:
            self.cart[food.id]['product'] = food
        #迭代字典的值list
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    @property
    def table_no(self):
        if self.table_no:
            return self.table_no
        return None

    @table_no.setter
    def table_no(self, table_no):
        self.table_no = table_no

    @property
    def message(self):
        if self.message:
            return self.message
        return None

    @message.setter
    def message(self, message):
        self.message = message