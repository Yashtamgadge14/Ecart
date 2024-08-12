from django.urls import path,include
from ecommapp import views
from ecommapp.views import simpleview
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [

   
    path('',views.home),
    path('contact/<a>',views.contact),
    path('about',views.about),
    path('myview',simpleview.as_view()),
    path('index',views.index),
    path('login',views.user_login),
    path("register",views.user_register),
    path('place_order',views.place_order),
    path('pd/<pid>',views.pd),
    path('cart',views.cart),
    path('logout',views.user_logout),
    path('catfilter/<cv>',views.catfilter),
    path('sort/<sv>',views.sort),
    path("range",views.range),
    path('addtocart/<pid>',views.addtocart),
    path('remove/<cid>',views.remove),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('makepayment',views.makepayment),
   
    
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)