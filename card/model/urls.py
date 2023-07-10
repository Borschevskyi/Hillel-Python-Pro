from django.urls import path
from .views import CardsView, create_card

urlpatterns = [
    path("card/", CardsView.as_view(http_method_names=["get", "post"]), name="card"),
    path("card/create/", create_card, name="create_card"),
]
