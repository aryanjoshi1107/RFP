from django.shortcuts import redirect,get_object_or_404
from django.views.generic import ListView
from django.views import View

from category.models import Category
from django.views.generic import CreateView,UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
# Create your views here.
   
class Categories(ListView):
    template_name= "categories.html"
    model = Category
    context_object_name = 'categories'
      
      
      
class AddCategory(LoginRequiredMixin,CreateView):
    """
    Api endpoint to   Add Categories  in the database
    """
    template_name='addcategory.html'
    model = Category
    context_object_name = "form"
    fields = ['name','description']
    success_url = reverse_lazy('Categories')
    
    def form_valid(self, form):
        form.instance.status = 'active'
        form.instance.created_by = self.request.user  
        messages.success(self.request, "The Category was created successfully.")       
        return  super(AddCategory,self).form_valid(form)
    
    
class ToggleStatus(LoginRequiredMixin, View):
    """
    Toggle the status of a Category and redirect back.
    Use POST only (safe for CSRF) and no separate template required.
    """
    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Category, pk=kwargs.get('pk'))
        if obj.created_by != request.user:
            messages.error(request, "You are not authorized to change this category.")
            return HttpResponseForbidden("Forbidden")

        # Toggle logic (adapt values to your choices: 'active'/'inactive' or 'active'/'deactive')
        obj.status = 'inactive' if obj.status == 'active' else 'active'
        obj.save(update_fields=['status'])

        messages.success(request, f"Category status changed to {obj.status}.")
        # Redirect back to where the request came from, or to a safe default
        next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or reverse_lazy('Categories')
        return redirect(next_url)

