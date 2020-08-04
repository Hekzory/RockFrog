from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template import loader
from FirstVer.settings import TEMPLATES
from .models import CardItem
from django.utils.datastructures import MultiValueDictKeyError


# Create your views here.
class MyInventoryView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/auth/login')
        context = dict()
        # context["inventory_items"] = request.user.inventory.carditem_set.all()[:16]
        context["inventory_items"] = CardItem.objects.filter(inventory=request.user.inventory)[:16].select_subclasses()
        # print(context["inventory_items"])
        items_count = request.user.inventory.carditem_set.count()
        context['extra_empty_slots'] = []
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

        template = loader.get_template("inventory/myinventory.html")
        return HttpResponse(template.render(context, request))


class GetItemView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({"response": "NotAuthenticated"})
        if request.POST["type"] == "card":
            try:
                item = CardItem.objects.get_subclass(id=int(request.POST["item_id"]))
            except CardItem.DoesNotExist:
                return JsonResponse({"response": "NoSuchItem"})
            except ValueError:
                return JsonResponse({"response": "IdNotANumber"})
            except MultiValueDictKeyError:
                return JsonResponse({"response": "IdNotANumber"})

        else:
            return JsonResponse({"response": "UnknownType"})
        if item.inventory.user.id != request.user.id:
            return JsonResponse({"response": "NotYourItem"})
        if request.POST["type"] == "card":
            return JsonResponse({"response": "ok", "item_name": item.name, "item_description": item.description,
                                 "item_rarity": item.rarity, "item_level": item.level, "item_maxlevel": item.maxlevel,
                                 "item_collected_cards": item.collected_cards,
                                 "points_per_level": item.increase_points_per_level_amount,
                                 "improvable_stats_list": item.get_improvable_stats_list(),
                                 "next_level_description": item.get_next_level_description()})


class IncreaseCardLevelView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({"response": "NotAuthenticated"})
        try:
            item = CardItem.objects.get(id=int(request.POST["item_id"]))
        except CardItem.DoesNotExist:
            return JsonResponse({"response": "NoSuchItem"})
        except ValueError:
            return JsonResponse({"response": "IdNotANumber"})
        if item.inventory.user.id != request.user.id:
            return JsonResponse({"response": "NotYourItem"})
        res = item.increase_level()
        return JsonResponse({"response": "ok", "item_name": item.name, "item_description": item.description,
                             "item_rarity": item.rarity, "item_level": item.level, "item_maxlevel": item.maxlevel,
                             "item_collected_cards": item.collected_cards,
                             "points_per_level": item.increase_points_per_level_amount})