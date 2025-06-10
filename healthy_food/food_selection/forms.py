from django import forms


class SearchNewFood(forms.Form):
    product = forms.CharField(label='produit recherché', required=True)


class ContactUsForm(forms.Form):
    first_name = forms.CharField(required=True)
    email = forms.EmailField()
    message = forms.CharField(max_length=1000)


class SaveProductForm(forms.Form):
    product_id = forms.CharField(widget=forms.HiddenInput(), required=True)
    # product_id = forms.CharField(required=True)

class TestForm(forms.Form):
    product_id = forms.CharField(required=True)
