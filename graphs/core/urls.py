from django.urls import path
from . import views

urlpatterns = [
    path('ajax_graph',views.ajax_alm_graph, name='ajax-alm'),

]