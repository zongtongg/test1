from django.urls import path

from apps.adverts.views import LocationView, CategoryView, test, SingleCategoryView, AdvertView

urlpatterns = [
    path('locations/<int:pk>/', LocationView.as_view()),
    path('categories/<int:pk>/', CategoryView.as_view()),
    path('<int:pk>/', test),
    path('category/<int:pk>/', SingleCategoryView.as_view()),
    path('advert/<int:pk>/', AdvertView.as_view()),
]