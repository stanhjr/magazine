from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from magazine.models import Product, ObjectBuyProduct, PurchaseReturn

from .models import MyUser
import pdb
pdb.set_trace()


class SignUpForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('username', 'password1', 'password2')


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
        # product_id = self.cleaned_data.get('age')


class PurchaseReturnForm(ModelForm):
    class Meta:
        model = PurchaseReturn
        fields = ()

    def clean(self):
        cleaned_data = super().clean()
        obj = self.cleaned_data.get('order')
        print(obj)





















