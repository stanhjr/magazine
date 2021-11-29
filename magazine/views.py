from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, FormView
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
    success_url = 'product.html'

    def form_valid(self, form):
        ...
    # Здесь будет логика после валидации


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
