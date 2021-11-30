import datetime
import decimal

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect, HttpResponse, request
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, FormView

from . import forms
from .forms import ProductCreateForm, SignUpForm, ProductBuyForm, PurchaseReturnForm
from .models import Product, ObjectBuyProduct, PurchaseReturn


class ProductListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Product
    template_name = 'index.html'
    login_url = 'login/'
    extra_context = {'create_form': ProductCreateForm()}

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('login/')


class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'magazine.view_choice'
    login_url = 'login/'
    http_method_names = ['post']
    form_class = ProductCreateForm
    success_url = '/'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return super().form_valid(form=form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ('product_name', 'product_description', 'product_count', 'image')
    template_name = 'update_form.html'
    success_url = '/'


class ProductListBuyView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'product.html'
    login_url = 'login/'
    extra_context = {'product_buy_form': ProductBuyForm()}


class ProductBuyView(LoginRequiredMixin, CreateView):
    login_url = 'login/'
    http_method_names = ['post', ]
    form_class = ProductBuyForm
    success_url = '/product'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        number_of_product = int(self.request.POST.get('number_of_product'))
        product_id = self.request.POST.get('product')
        obj.product = Product.objects.get(id=product_id)
        obj.user.online_wallet -= decimal.Decimal(float(obj.product.product_price)) * number_of_product
        obj.product.product_count -= number_of_product
        obj.product.save()
        obj.user.save()
        obj.save()
        return super().form_valid(form=form)


# Дописать валидацию отправки возврата !
class OrderReturnCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login/'
    http_method_names = ['post', ]
    form_class = PurchaseReturnForm
    success_url = '/order'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.object_buy_product = form.object_buy
        obj.save()
        return super().form_valid(form=form)

    def get_form_kwargs(self):
        kw = super(OrderReturnCreateView, self).get_form_kwargs()
        kw['request'] = self.request
        return kw

    def form_invalid(self, form):
        return HttpResponseRedirect(reverse('order'))


class OrderListView(LoginRequiredMixin, ListView):
    model = ObjectBuyProduct
    template_name = 'order.html'
    login_url = 'login/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        if 'error_text' in self.request.session and 'order_id' in self.request.session:
            context.update(
                {
                    'error_text': self.request.session['error_text'],
                    'order_id': self.request.session['order_id'],
                 }
            )
            del self.request.session['error_text']
            del self.request.session['order_id']
        return context


# здесь в экстраконтенте две формы или что?
class OrderAdmin(LoginRequiredMixin, ListView):
    model = PurchaseReturn
    template_name = 'purchase-return.html'
    login_url = 'login/'


# Доделать форму без форм класс
class ReturnUserDelete(LoginRequiredMixin, FormView):
    form_class = PurchaseReturnForm
    http_method_names = ['post', ]
    success_url = '/order-admin'

    def form_valid(self, form):
        purchase_id = self.request.POST.get('purchase_id')
        obj_purchase_return = PurchaseReturn.objects.get(id=purchase_id)
        obj_purchase_return.delete()
        return super().form_valid(form=form)


# Доделать форму без форм класс
class ReturnUserConfirm(LoginRequiredMixin, FormView):
    form_class = PurchaseReturnForm
    http_method_names = ['post', ]
    success_url = '/order-admin'

    def form_valid(self, form):
        obj = form.save(commit=False)
        order_id = self.request.POST.get('return_id')
        purchase_id = self.request.POST.get('purchase_id')
        object_buy_product = ObjectBuyProduct.objects.get(id=order_id)
        obj_purchase_return = PurchaseReturn.objects.get(id=purchase_id)
        object_buy_product.product.product_count += int(object_buy_product.number_of_product)
        obj.user = self.request.user
        obj.user.online_wallet += decimal.Decimal(
            float(object_buy_product.product.product_price) * float(object_buy_product.number_of_product))
        obj.user.save()
        object_buy_product.product.save()
        obj_purchase_return.delete()
        object_buy_product.delete()
        return super().form_valid(form=form)


class Login(LoginView):
    success_url = '/'
    template_name = 'login.html'


class Register(CreateView):
    form_class = SignUpForm
    template_name = 'register.html'
    success_url = '/'


class Logout(LoginRequiredMixin, LogoutView):
    next_page = '/'
    login_url = 'login/'
