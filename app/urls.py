from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import *


urlpatterns = [
    #path('', views.home),
    path('', views.ProductView.as_view(),name="home"),
    path('product-detail/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.show_cart, name='show_cart'),
     path('pluscart/', views.pluscart, name='pluscart'),
    path('minuscart/', views.minuscart),
    path('removecart/<int:pk>', views.removecart),
    path('buy-now/<int:pk>', views.buyNow, name='buy-now'),
    path('profile/',views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    #path('changepassword/', views.change_password, name='changepassword'),
    #path('login/', views.login, name='login'),
    path('accounts/login/',auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm),name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone/'),
         name='passwordchange'),
    path('passwordchangedone/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),

    path('passwordreset/',auth_views.PasswordResetView.as_view(template_name='app/passwordreset.html',form_class=MyPasswordResetForm),
          name='passwordreset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='app/passwordresetdone.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='app/passwordresetconfirm.html',form_class=MySetPasswodForm),name='password_reset_confirm'),
    path('passwordresetcomplete/',auth_views.PasswordResetCompleteView.as_view(template_name='app/passwordresetcomplete.html'),name='password_reset_complete'),

    #path('registration/', views.customerregistration, name='customerregistration'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),

    path('checkout/', views.checkout, name='checkout'),

    path('paymentdone/', views.paymentdone, name='paymentdone'),

    path('mobile/', views.MobileView, name='mobile'),
    path('mobile/<slug:data>/', views.MobileView, name='mobiledata'),
    path('mobile/<int:num>', views.MobileView, name='mobiledata'),

    path('laptop/',views.laptopView,name='laptop'),
    path('laptop/<slug:data>/', views.laptopView, name='laptopdata'),

    path('topwear/',views.topwearView,name='topwear'),
    path('topwear/<slug:data>/', views.topwearView, name='topweardata'),

    path('bottomwear/',views.bottomwearView,name='bottomwear'),
    path('bottomwear/<slug:data>/', views.bottomwearView, name='bottomweardata'),

    path('wishlist/',views.wishlistView,name='wishlist'),
    path('addtowishlist/<int:pk>',views.addToWishlistView,name='addtowishlist'),
    path('removewishlist/<int:pk>',views.removeWishlistView,name='removewishlist')
   

    






] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
