from django import forms

class AddressForm(forms.Form):
    address_form = forms.CharField(label='Enter Address', max_length=500)