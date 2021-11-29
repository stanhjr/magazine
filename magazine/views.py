import decimal

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, FormView
from .forms import ProductCreateForm, SignUpForm, ProductBuyForm, PurchaseReturnForm
from .models import Product, ObjectBuyProduct, PurchaseReturn


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'index.html'
    login_url = 'login/'
    extra_context = {'create_form': ProductCreateForm()}


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


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = '/'


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


class OrderReturnCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login/'
    http_method_names = ['post', ]
    form_class = PurchaseReturnForm
    success_url = '/order'

    def form_valid(self, form):
        obj = form.save(commit=False)
        order_id = self.request.POST.get('order')
        obj.object_buy_product = ObjectBuyProduct.objects.get(id=order_id)
        obj.user = self.request.user
        print(obj)
        obj.save()
        return super().form_valid(form=form)


class OrderListView(LoginRequiredMixin, ListView):
    model = ObjectBuyProduct
    template_name = 'order.html'
    login_url = 'login/'
    extra_context = {'order_return_form': PurchaseReturnForm()}


class OrderReturnListView(LoginRequiredMixin, ListView):
    model = PurchaseReturn
    template_name = 'product.html'
    login_url = 'login/'
    extra_context = {'order_return_form': PurchaseReturnForm()}


# здесь в экстраконтенте две формы или что?
class OrderUser(LoginRequiredMixin, ListView):
    model = PurchaseReturn
    template_name = 'purchase-return.html'
    login_url = 'login/'
    # extra_context = {'confirm_form': PurchaseConfirmForm()}











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
