from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from magazine.models import Product, ObjectBuyProduct

from .models import MyUser


class SignUpForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('username', 'password1', 'password2', 'avatar')


class ProductCreateForm(ModelForm):
    class Meta:
        model = Product
        fields = ('product_name', 'product_description', 'product_count', 'image')


class ProductBuyForm(ModelForm):
    class Meta:
        model = ObjectBuyProduct
        fields = ('number_of_product', 'product_name', 'user')

    # def clean(self):
    #     cleaned_data = super().clean()
    #     print(cleaned_data)
        # product_count = int(self.cleaned_data.get('product_count'))
        # print(product_count)
        # product_price = int(self.cleaned_data.get('product_price'))
        # product_need_buy = int(self.cleaned_data.get('number_of_product'))
        # print(product_need_buy)
        #
        # if product_count < product_need_buy:
        #     raise ValidationError('Такого количества продукции на складе нет')
        # if product_price * product_need_buy > float(self.request.user.online_wallet):
        #     raise ValidationError('Недостаточное количество денег в кошельке, ваш остаток: ', self.request.user.online_wallet)


