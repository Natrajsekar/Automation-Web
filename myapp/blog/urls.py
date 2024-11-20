from django.urls import path
from . import views
from .views import ccms_file,rmr_file,rr_file,receipt_script,challan_file,challan_script,cash_file,cash_script
app_name ='blog'

urlpatterns = [
    path("",views.index,name='index'),
    path("post/<str:post_id>",views.detail,name='detail'),
    path("old_url",views.old_url_redirect,name='old_url'),
    path("new_some_url",views.new_url_view,name='new_one'),
    path("run page",views.run_page,name='runpage'),
    path('CCMS/', ccms_file, name='upload_file'),
    path('RMR/', rmr_file, name='rmr_upload_file'),
    path('receipt/',rr_file,name='re_2'),
    path('challan/',challan_file,name='ch_file'),
    path('cash/',cash_file,name='ca_file'),
    path('ccms_script/', views.ccms_script, name='run_script'),
    path('rmr_script/', views.rmr_script, name='rmr_script'),
    path('receipt_script/', views.receipt_script, name='receipt_script'),
    path('challan_script/', views.challan_script, name='challan_script'),
    path('cash_script/', views.cash_script, name='cash_script')
]


