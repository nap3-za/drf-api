from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from knox import views as knox_views

from account import views as account_views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('authentication/', include('knox.urls')),
    path('authentication/sign-up/', account_views.SignUpView.as_view(), name="sign-up"),
    path('authentication/sign-in/', account_views.SignInView.as_view(), name="sign-in"),
    
    # Sends account data using received apiToken
    path('authentication/account/', account_views.RetrieveAccount.as_view(), name="retrieve-account"),
        
    path('account/', include('account.urls', namespace="account")),

    # Password reset defaults
    path('password-reset/', auth_views.PasswordResetView.as_view(), name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),    
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(),name='password_change'),

]
