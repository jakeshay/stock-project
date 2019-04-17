import requests
from django.shortcuts import render, get_object_or_404, redirect
from .models import Stock
from django.http import HttpResponse
from .forms import StockForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def index(request):
	if request.method == 'POST':
		form = StockForm(request.POST)
		form.user = request.user
		form.save()

	form = StockForm()


	stocks = Stock.objects.all()

	stock_data = []

	recent = Stock.objects.order_by('-date_added')[:5]

	recent_list = []

	for element in recent:
		recent_info = {
			'symbol' : element.symbol,
		}

		recent_list.append(recent_info)

	for stock in stocks:

		stock_info = {
			'symbol' : stock.symbol,
		}

		stock_data.append(stock_info)

	context = {'stock_data' : stock_data, 'recent_list' : recent_list, 'form': form}
	return render(request, 'stock_analysis/stock_analysis.html', context)


@login_required(login_url="/accounts/login/")
def detail(request, symbol):
	url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&apikey=H9DJDZCX30HXOG11'

	stock = Stock.objects.get(symbol=symbol)


	stock_data = []

	r = requests.get(url.format(stock)).json()

	dis = r['Time Series (Daily)']
	first = next(iter(dis))

	stock_info = {
		'symbol' : stock.symbol,
		'open' : dis[first]['1. open'],
		'close' : dis[first]['4. close'],
		'high' : dis[first]['2. high'],
		'low' : dis[first]['3. low'],
		'volume' : dis[first]['5. volume'],
	}

	stock_data.append(stock_info)


	context = {'stock_data' : stock_data}
	return render(request, 'stock_analysis/detail.html', context)

@login_required(login_url="/accounts/login/")
def myStocks(request):
	stocks = Stock.objects.filter(user_id=request.user)

	stock_data = []

	for stock in stocks:

		stock_info = {
			'symbol' : stock.symbol,
		}

		stock_data.append(stock_info)

	context = {'stock_data' : stock_data}
	return render(request, 'stock_analysis/view_stocks.html', context)

@login_required(login_url="/accounts/login/")
def addStocks(request):
	if request.method == 'POST':
		form = StockForm(request.POST)
		form.user = request.user
		form.save()

	form = StockForm()

	context = {'form': form}
	return render(request, 'stock_analysis/addstocks.html', context)

def deleteStocks(request, symbol):
	stock = get_object_or_404(Stock, symbol=symbol)
	stock.delete()
	return redirect("/mystocks")

@login_required(login_url="/accounts/login/")
def analysis(request):
	url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&apikey=H9DJDZCX30HXOG11'

	stocks = Stock.objects.all()

	stock_data = []
	max_price_change = []
	min_price_change = []
	volumes = []
	for stock in stocks:
		r = requests.get(url.format(stock)).json()

		dis = r['Time Series (Daily)']
		first = next(iter(dis))
		change = (float(dis[first]['2. high']) - float(dis[first]['3. low']))/float(dis[first]['2. high'])
		change *= 100

		stock_info = {
			'symbol' : stock.symbol,
			'volume' : dis[first]['5. volume'],
			'change' : change,
		}

		stock_data.append(stock_info)

	max_price_change = sorted(stock_data, key = lambda i: i['change'], reverse=True)[:5]
	min_price_change = sorted(stock_data, key = lambda i: i['change'])[:5]
	volumes = sorted(stock_data, key = lambda i: i['volume'])[:5]
	context = {'max_price_change' : max_price_change, 'min_price_change' : min_price_change, 'volumes' : volumes}
	return render(request, 'stock_analysis/analysis.html', context)