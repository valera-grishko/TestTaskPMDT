from django.urls import path
from . import views

urlpatterns = [
    path("categories", views.ShowCategories.as_view(), name='categories'),
    path("cards/<int:pk>", views.ShowCards.as_view(), name='cards'),
    path("detail/<int:pk>", views.ShowCardDetail.as_view(), name='detail'),
    path("products/<int:pk>", views.ShowProducts.as_view(), name='products'),
]