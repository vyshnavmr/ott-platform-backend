from django.urls import path
from app import views

urlpatterns = [
    path('',views.adminlogin, name='adminlogin'),
    path('home/',views.home, name='home'),
    path('block-user/<int:user_id>/', views.blockuser, name='blockuser'),
    path('unblock-user/<int:user_id>/', views.unblockuser, name='unblockuser'),
    path('changepassword/',views.changepassword, name='changepassword'),
    path('addmovie/',views.addmovie, name='addmovie'),
    path('userlist/',views.userlist, name='userlist'),
    path('movielist/',views.movielist, name='movielist'),
    path('editmovie/<int:movie_id>/',views.edit_movie,name='editmovie'),
    path('history/<int:user_id>/',views.user_history,name='user_history'),
    path('reports/', views.reports, name='reports'),
    path("logout/", views.adminlogout, name="logout"),
]


