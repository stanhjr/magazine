from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from magazine.models import Product, ObjectBuyProduct, PurchaseReturn

from .models import MyUser


class SignUpForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('username', 'password1', 'password2')


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('product_name', 'product_description', 'product_price', 'product_count', 'image')


class ProductBuyForm(forms.ModelForm):
    class Meta:
        model = ObjectBuyProduct
        fields = ('number_of_product',)

    def clean(self):
        cleaned_data = super().clean()
        # product_id = self.cleaned_data.get('age')


class PurchaseReturnForm(forms.ModelForm):
    order = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PurchaseReturnForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PurchaseReturn
        fields = ()

    def clean(self):
        cleaned_data = super().clean()
        try:
            object_buy = ObjectBuyProduct.objects.get(id=cleaned_data.get('order'))
        except ObjectBuyProduct.DoesNotExist:
            object_buy = None
        except ObjectBuyProduct.MultipleObjectsReturned:
            object_buy = None
        if object_buy and hasattr(object_buy, 'return_object'):
            error_text = 'Return already exist'
            self.add_error(None, error_text)
            self.request.session['error_text'] = error_text
            self.request.session['order_id'] = object_buy.pk
        else:
            self.object_buy = object_buy
