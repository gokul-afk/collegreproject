from django.urls import path
from main import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.home,name='home'),
    path('men/<str:cat>',views.men,name='men'),
    path('signup',views.signup,name='signup'),
    path('woman/<str:cat>',views.woman,name='woman'),
    path('product_details/<int:pk>',views.product_details,name='product_details'),
    path('addtocart/<int:pk>',views.addtocart,name="addtocart"),
    path('wish/<int:pk>',views.wish,name="wish"),
    path('order/',views.order,name="order"),
    path('login/',views.login,name="login"),
    path('bag/',views.bag,name="bag"),
    path('showorders/',views.showorders,name="showorders"),
    path('wishlist/',views.wishlist,name="wishlist"),
    path('deletecart/<int:pk>',views.deletecart,name="deletecart"),
    path('logout/',views.logout,name="logout"),
    path('deleteorder/<int:pk>',views.deleteorder,name="deleteorder"),
]
