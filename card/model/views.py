import json
from django.http import HttpRequest, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from .models import Cards


class CardsView(View):
    def get(self, request: HttpRequest):
        cards = Cards.objects.all()
        json_response = {
            "cards": [
                {
                    "pan": str(card.pan),
                    "expiration_date": str(card.expiration_date),
                    "cvv": str(card.cvv),
                    "owner_id": str(card.owner_id),
                    "status": str(card.status),
                }
                for card in cards
            ]
        }
        if request.headers["accept"] == "application/json":
            return JsonResponse(json_response)
        else:
            context = {
                "cards": [
                    {
                        "pan": card.pan,
                        "expiration_date": card.expiration_date,
                        "cvv": card.cvv,
                        "owner_id": card.owner_id,
                        "status": card.status,
                    }
                    for card in cards
                ]
            }
            return render(request, "cards/cards_list.html", context, "text/html")

    def post(self, request: HttpRequest):
        body = json.loads(request.body)
        card = Cards.objects.create(
            pan=body["pan"],
            expiration_date=body["expiration_date"],
            cvv=body["cvv"],
            status=body["status"],
        )
        card.save()
        return JsonResponse({"id": str(card.id)})


def create_card(request):
    if request.method == "GET":
        cards = Cards.objects.all()
        return render(request, "cards/create_card.html", {"cards": cards})
    elif request.method == "POST":
        Cards.objects.create(
            pan=request.POST["pan_card"],
            expiration_date=request.POST["expiration_date_card"],
            cvv=request.POST["cvv_card"],
            status=request.POST["status_card"],
        )
        return HttpResponseRedirect(reverse("card"))
