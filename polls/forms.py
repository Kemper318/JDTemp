from django import forms
    
class ScanQRForm(forms.Form):
    qr_code = forms.CharField(max_length=50, required=True)

class CheckInForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    street_address = forms.CharField(max_length=50, required=True)
    city = forms.CharField(max_length=50, required=True)
    zip_code = forms.CharField(max_length=50, required=True)