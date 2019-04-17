from django.forms import ModelForm, TextInput
from .models import Stock

class StockForm(ModelForm):
	class Meta:
		model = Stock
		fields = ['symbol'] 
		widgets = {'symbol' : TextInput(attrs={'class' : 'input', 'placeholder' : 'Stock'})}
