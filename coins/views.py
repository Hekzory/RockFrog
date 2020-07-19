from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.views.generic import View
from .forms import *


class CoinManagementView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/")
        else:
            coins = request.user.profile.coinmanagement.coins
            transactions_list = request.user.profile.coinmanagement.transaction_set.order_by('-time_created')[:5]
            template = loader.get_template('coins/coin_management.html')
            context = {'coins': coins, 'transaction_list': transactions_list}
            return HttpResponse(HttpResponse(template.render(context, request)))


class TransactionHistoryView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/")
        else:
            transactions_list = request.user.profile.coinmanagement.transaction_set.order_by('-time_created')
            paginator = Paginator(transactions_list, 10)
            page_number = request.GET.get('page')
            try:
                page = paginator.page(page_number)
            except PageNotAnInteger:
                page = paginator.page(1)
            except EmptyPage:
                page = paginator.page(paginator.num_pages)
            template = loader.get_template('coins/transaction_history.html')
            context = {'transaction_list': transactions_list, 'page': page}
            return HttpResponse(HttpResponse(template.render(context, request)))
