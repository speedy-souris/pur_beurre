from django import forms
class SearchNewFood(forms.Form):
   produit = forms.CharField(required=True)

class ContactUsForm(forms.Form):
   first_name = forms.CharField(required=True)
   email = forms.EmailField()
   message = forms.CharField(max_length=1000)