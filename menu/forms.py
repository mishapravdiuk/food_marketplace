from django import forms
from .models import Category

# Category crud form 
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']