from django import forms

class CCMS(forms.Form):
    myfile = forms.FileField(label='Select a file')

class RMR(forms.Form):
    myfile_rmr = forms.FileField(label='Select a file')

class Receipt_1(forms.Form):
    first_file = forms.FileField(label='Select a file')
    second_file = forms.FileField(label='Select a file')
    third_file = forms.FileField(label='Select a file')
    four_file = forms.FileField(label='Select a file')
    five_file = forms.FileField(label='Select a file')
    six_file = forms.FileField(label='Select a file')
    seven_file = forms.FileField(label='Select a file')
    eight_file = forms.FileField(label='Select a file')
    nine_file = forms.FileField(label='Select a file')
    ten_file = forms.FileField(label='Select a file')

class challan_status(forms.Form):
    first = forms.FileField(label='Select a file')
    second = forms.FileField(label='Select a file')
    third = forms.FileField(label='Select a file')
    four = forms.FileField(label='Select a file')
    five = forms.FileField(label='Select a file')
    six= forms.FileField(label='Select a file')
    seven = forms.FileField(label='Select a file')

class cash_deposition(forms.Form):
    first = forms.FileField(label='Select a file')
    second = forms.FileField(label='Select a file')
    third = forms.FileField(label='Select a file')
    four = forms.FileField(label='Select a file')
    five = forms.FileField(label='Select a file')
    six= forms.FileField(label='Select a file')
    seven = forms.FileField(label='Select a file')

