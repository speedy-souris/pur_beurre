from django import forms


class SearchNewFood(forms.Form):
    product = forms.CharField(label='produit recherché', required=True)


class ContactUsForm(forms.Form):
    first_name = forms.CharField(required=True)
    email = forms.EmailField()
    message = forms.CharField(max_length=1000)
