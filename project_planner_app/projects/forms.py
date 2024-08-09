"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import Projects,data_container,data_items

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))
 
class DataContainerForm(forms.ModelForm):
    class Meta:
        model = data_container
        fields = '__all__'
        exclude = ['created_by','project_ID','level','is_root']
"""
class BookForm(forms.Form):

    title = forms.CharField(label = "Title", widget = forms.TextInput( attrs={'class': 'form-control'} ))
    author = forms.CharField(label = "Author", widget = forms.TextInput( attrs={'class': 'form-control'} ))
    description = forms.CharField(label = "Description", widget = forms.Textarea( attrs={'class': 'form-control', 'rows': '5'} ))
    year = forms.CharField(label = "Year", widget = forms.NumberInput( attrs={'class': 'form-control'} ))

    #validation
    def clean(self):
        super(BookForm, self).clean()

        title = self.cleaned_data.get('title')

        if len(title)<5:
            self.add_error('title','Can not save title less than 5 characters long')
            self.fields['title'].widget.attrs.update({'class': 'form-control  is-invalid'})

        return self.cleaned_data       
"""
