from django.urls import path
from . import views

urlpatterns = [
    
    path('signup/', views.Signup, name='signup'),
    path('login/', views.login, name='login'),
    path('movie/search/', views.search_movie, name='search_movie'),
    path('listmovie/', views.list_movie, name='list_movie'),
    path('movie/details/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movie/watch/<int:movie_id>/', views.watch_movie, name='movie_watch'),
    path('watchlist/', views.get_watchlist, name='get_watchlist'),
    path('watchlist/add/<int:movie_id>/', views.add_watchlist, name='add_watchlist'),
    path('watchlist/delete/<int:movie_id>/', views.delete_from_watchlist, name='delete_from_watchlist'),
    path('watchhistory/', views.get_watchhistory, name='get_watchhistory'),
    path('changepassword/', views.change_password, name='change_password'),
]