from django import forms
from .models import User


class AddressForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['address', 'code_postal', 'phone_number']
        widgets = {
            'address': forms.TextInput(attrs={
                'class': 'w-full border border-outline-variant rounded-lg px-4 py-3 text-body-md font-body-md text-on-surface bg-surface-container-lowest focus:ring-0 focus:border-primary transition-colors placeholder-on-surface-variant/50',
                'placeholder': 'Enter your address',
            }),
            'code_postal': forms.TextInput(attrs={
                'class': 'w-full border border-outline-variant rounded-lg px-4 py-3 text-body-md font-body-md text-on-surface bg-surface-container-lowest focus:ring-0 focus:border-primary transition-colors placeholder-on-surface-variant/50',
                'placeholder': 'Enter postal code',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full border border-outline-variant rounded-lg px-4 py-3 text-body-md font-body-md text-on-surface bg-surface-container-lowest focus:ring-0 focus:border-primary transition-colors placeholder-on-surface-variant/50',
                'placeholder': 'Enter phone number',
            }),
        }
        labels = {
            'address': 'Address',
            'code_postal': 'Postal Code',
            'phone_number': 'Phone Number',
        }