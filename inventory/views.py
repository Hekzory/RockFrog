from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template import loader
from FirstVer.settings import TEMPLATES
from .models import CardItem


# Create your views here.
class MyInventoryView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/auth/login')
        context = dict()
        context["inventory_items"] = request.user.inventory.carditem_set.all()[:16]
        items_count = request.user.inventory.carditem_set.count()
        context['extra_empty_slots'] = 0
        context['more_than_one_page'] = False
        if items_count <= 16:
            rows = items_count//4+1
            if items_count % 4 == 0:
                rows -= 1
            else:
                context['extra_empty_slots'] = range(4 - (items_count % 4))
        else:
            rows = 4
            context["more_than_one_page"] = True

        print(items_count, rows, context['extra_empty_slots'])
        template = loader.get_template("inventory/myinventory.html")
        return HttpResponse(template.render(context, request))


class GetItemView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({"response": "NotAuthenticated"})
        if request.POST["type"] == "card":
            try:
                item = CardItem.objects.get(id=int(request.POST["item_id"]))
            except CardItem.DoesNotExist:
                return JsonResponse({"response": "NoSuchItem"})
            except ValueError:
                return JsonResponse({"response": "IdNotANumber"})
        else:
            return JsonResponse({"response": "UnknownType"})
        if item.inventory.user.id != request.user.id:
            return JsonResponse({"response": "NotYourItem"})
        if request.POST["type"] == "card":
            return JsonResponse({"response": "ok", "item_name": item.name, "item_description": item.description, "item_rarity": item.rarity})
