from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'departamento_app'

urlpatterns = [
    path(
        'departamento-lista',
        views.DepatarmentoListView.as_view(),
        name='departamento_list'
    ),
    path(
        'new-departamento',
        views.NewDepartamentoView.as_view(),
        name='nuevo_departamento'
    )

]
