from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from magazine.models import Product, ObjectBuyProduct

from .models import MyUser


class SignUpForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('username', 'password1', 'password2',  'avatar')


class ProductCreateForm(ModelForm):
    class Meta:
        model = Product
        fields = ('product_name', 'product_description', 'product_price', 'product_count', 'image')


class ProductBuyForm(ModelForm):
    class Meta:
        model = ObjectBuyProduct
        fields = ('number_of_product', )

    def clean(self):
        cleaned_data = super().clean()









