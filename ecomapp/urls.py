from django.urls import path
from ecomapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('product',views.product),
    path('register',views.register),
    path('login',views.user_login),
    path('logout',views.user_logout),
    path('catfilter/<cv>',views.catfilter),
    path('sort/<sv>',views.sort),
    path('pricefilter',views.pricefilter),
    path('search',views.search),
    path('product_detail/<pid>',views.product_detail),
    path('addtocart/<pid_id>',views.addtocart),
    path('cart',views.viewcart),
    path('updateqty/<x>/<cid>',views.updateqty),
    path('remove/<cid>',views.removecart),
    path('placeorder',views.placeorder),
    path('fetchorder',views.fetchorder),
    path("makepayment",views.makepayment),
    path('paymentsuccess',views.success),

]

urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
