# views.py
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegisterForm, VendorDetailsForm,LoginForm
from users.models import Users, VendorDetails
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
# views.py
from django.views.generic import FormView
from .forms import UserRegisterForm, VendorDetailsForm




class Register(FormView):
    template_name = 'register.html'
    success_url = reverse_lazy('Login')

    def get_form_class(self):
        return UserRegisterForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_vendor = self.request.resolver_match.url_name == 'vendor-register'
        context['is_vendor'] = is_vendor
        if is_vendor:
            context['vendor_form'] = VendorDetailsForm()
        return context

    def post(self, request, *args, **kwargs):
        user_form = UserRegisterForm(request.POST)
        is_vendor = request.resolver_match.url_name == 'vendor-register'
        vendor_form = VendorDetailsForm(request.POST) if is_vendor else None

        if user_form.is_valid() and (not is_vendor or vendor_form.is_valid()):
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.role = 'vendor' if is_vendor else 'admin'
            user.save()

            if is_vendor:
                vendor = vendor_form.save(commit=False)
                vendor.user = user
                vendor.save()
            return self.form_valid(user_form)

        context = self.get_context_data()
        context['form'] = user_form
        if is_vendor:
            context['vendor_form'] = vendor_form
        return self.render_to_response(context)
    

class MyLoginView(View):
    template_name = 'login.html'
    def get(self, request):
        return render(request, self.template_name, {'form': LoginForm()})
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                print("Logged in:", user.email)
                request.session['role'] = user.role  # storing role in session to load content dynamically in dashboard
                return redirect('Dashboard')  
            else:
                form.add_error(None, "Invalid email or password")

        return render(request, self.template_name, {'form': form})

   
class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"
    

    
    