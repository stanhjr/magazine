from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from .forms import ProductCreateForm, SignUpForm, ProductBuyForm
from .models import Product, ObjectBuyProduct


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
    fields = ('product_name', 'product_description', 'product_count', 'image', 'number_of_product')
    template_name = 'update_form.html'
    success_url = '/'


class ProductListBuyView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'product.html'
    login_url = 'login/'
    extra_context = {'product_buy_form': ProductBuyForm()}


class ProductBuyView(LoginRequiredMixin, CreateView):
    login_url = 'login/'
    http_method_names = ['post']
    form_class = ProductBuyForm
    success_url = '/'

    def form_valid(self, form):
        print(form)
        obj = form.save(commit=False)
        print(obj)
        # product_count = int(obj.form_class.product_name.product_count)
        # product_price = int(obj.form_class.product_name.product_price)
        # product_need_buy = int(self.form_class.number_of_product)
        # #
        # # product_count = float(self.form_class.product_name.product_count)
        # # product_price = float(self.form_class.product_name.product_price)
        # # product_need_buy = float(self.form_class.number_of_product)
        #
        # self.request.user.online_wallet -= product_price * product_need_buy
        # product_count -= product_need_buy
        # obj.save()
        # return super().form_valid(form=form)


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
