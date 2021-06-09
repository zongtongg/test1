from django.urls import path

from adverts.views import RegionView, CategoryView, test, SingleCategoryView

urlpatterns = [
    path('regions/<int:pk>/', RegionView.as_view()),
    path('categories/<int:pk>/', CategoryView.as_view()),
    path('', test),
    path('category/<int:pk>/', SingleCategoryView.as_view()),
]