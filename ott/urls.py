from django.contrib import admin
from django.urls import path, include
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('',views.adminlogin),
    # path('home/',views.home, name='home'),
    # path('block-user/<int:user_id>/', views.blockuser, name='blockuser'),
    # path('unblock-user/<int:user_id>/', views.unblockuser, name='unblockuser'),
    # path('changepassword/',views.changepassword, name='changepassword'),
    # path('addmovie/',views.addmovie, name='addmovie'),
    # path('userlist/',views.userlist, name='userlist'),


    path('', include('app.urls')),
    path('userapi/', include('userapi.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

