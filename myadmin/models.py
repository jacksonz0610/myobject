from django.db import models
from datetime import datetime

# Create your models here.
# 员工信息模型
class User(models.Model):
    username = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    password_hash = models.CharField(max_length=100)
    password_salt = models.CharField(max_length=50)
    status = models.IntegerField(default=1)# 1正常2禁用6管理员9删除
    create_at = models.DateTimeField(default=datetime.now)
    update_at = models.DateTimeField(default=datetime.now)

    def toDict(self):
        return {'id': self.id, 'username': self.username, 'nickname': self.nickname,
                'password_hash': self.password_hash, 'password_salt': self.password_salt,
                'status': self.status, 'create_at': self.create_at.strftime('%Y-%m-%d %H:%M:%S'),
                'update_at': self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = 'user'

# 店铺信息模型
class Shop(models.Model):
    name = models.CharField(max_length=255)
    cover_pic = models.CharField(max_length=255)
    banner_pic = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    status = models.IntegerField(default=1)# 1正常2暂停9删除
    create_at = models.DateTimeField(default=datetime.now)
    update_at = models.DateTimeField(default=datetime.now)

    def toDict(self):
        shopname = self.name.split('-')
        return {'id': self.id, 'name': shopname[0], 'shop': shopname[1], 'cover_pic': self.cover_pic,
                'banner_pic': self.banner_pic, 'address': self.address,
                'phone': self.phone, 'status': self.status,
                'create_at': self.create_at.strftime('%Y-%m-%d %H:%M:%S'),
                'update_at': self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = 'shop'

# 菜品分类信息模型
class Category(models.Model):
    shop_id = models.IntegerField()
    name = models.CharField(max_length=50)
    status = models.IntegerField(default=1)
    create_at = models.DateTimeField(default=datetime.now)
    update_at = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = 'category'


# 菜品信息模型
class Product(models.Model):
    shop_id = models.IntegerField()
    category_id = models.IntegerField()
    cover_pic = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    price = models.FloatField()
    status = models.IntegerField(default=1)
    create_at = models.DateTimeField(default=datetime.now)
    update_at = models.DateTimeField(default=datetime.now)

    def toDict(self):
        return {'id': self.id, 'shop_id': self.shop_id, 'category_id': self.category_id,
                'cover_pic': self.cover_pic, 'name': self.name, 'price': self.price, 'status': self.status,
                'create_at': self.create_at.strftime('%Y-%m-%d %H:%M:%S'),
                'update_at': self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = 'product'

# 会员信息管理
class Member(models.Model):
    nickname = models.CharField(max_length=50)
    avatar = models.CharField(max_length=255)
    mobile = models.CharField(max_length=50)
    status = models.IntegerField(default=1) # 状态：1正常2禁用9删除
    create_at = models.DateTimeField(default=datetime.now)
    update_at = models.DateTimeField(default=datetime.now)

    def toDict(self):
        return {'id': self.id, 'nickname': self.nickname, 'avatar': self.avatar,
                'mobile': self.mobile, 'status': self.status, 'create_at': self.create_at.strftime('%Y-%m-%d %H:%M:%S'),
                'update_at': self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = 'member'


# 订单模型
class Orders(models.Model):
    shop_id = models.IntegerField()
    member_id = models.IntegerField()
    user_id = models.IntegerField()
    money = models.FloatField()
    status = models.IntegerField(default=1)# 订单状态：1过程中2无效3已完成
    payment_status = models.IntegerField(default=1)# 支付状态：1未支付2已支付3已退款
    create_at = models.DateTimeField(default=datetime.now)
    update_at = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = 'orders'


# 订单详情模型
class OrderDetail(models.Model):
    order_id = models.IntegerField()
    # product_id = models.IntegerField()
    product = models.ForeignKey('Product', on_delete=models.CASCADE)  # 多对一
    product_name = models.CharField(max_length=50)
    price = models.FloatField()
    quantity = models.IntegerField()
    status = models.IntegerField(default=1)# 订单状态：1正常9删除

    class Meta:
        db_table = 'order_detail'


# 支付信息模型
class Payment(models.Model):
    order_id = models.IntegerField()
    member_id = models.IntegerField()
    money = models.FloatField()
    type = models.IntegerField()
    bank = models.IntegerField(default=1)# 1微信2余额3现金4支付宝
    status = models.IntegerField(default=1)# 1未支付2已支付3已退款
    create_at = models.DateTimeField(default=datetime.now)
    update_at = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = 'payment'


# 会员地址模型
class Address(models.Model):
    member_id = models.IntegerField()
    name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=11)
    province = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    district = models.CharField(max_length=20)
    detail = models.CharField(max_length=255)
    postalCode = models.CharField(max_length=10)
    status = models.IntegerField()# 状态1正常9删除

    def toDict(self):
        return {'id': self.id, 'member_id': self.member_id, 'name': self.name, 'mobile': self.mobile,
                'province': self.province, 'city': self.city, 'district': self.district,
                'detail': self.detail, 'postalCode': self.postalCode, 'status': self.status}

    class Meta:
        db_table = 'address'
