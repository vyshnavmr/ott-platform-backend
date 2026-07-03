from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from django.db.models import F
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.authtoken.models import Token
from app.models import User, Movie, WatchList, WatchHistory
from .serializers import MovieSerializer, WatchListSerializer, WatchHistorySerializer


#! 65ef6f3eca0d8900933fafab8e21acc9694aa61e

#! SIGNUP / REGISTER
@api_view(['POST'])
@permission_classes((AllowAny,))
def Signup(request):
    
    email  = request.data.get("email")
    password = request.data.get("password")
    name = request.data.get("name")

    if not name or not email or not password:
        return Response({'message':'All fields are required'})
    if User.objects.filter(email=email).exists():
        return  JsonResponse({'message':'Email already exist'})
    
    user = User.objects.create_user(email=email,password=password)
    user.name = name
    user.save()

    return JsonResponse({'message':'user created successsfully'} ,status = status.HTTP_201_CREATED)


#! LOGIN
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    
    email = request.data.get("email")
    password = request.data.get("password")
    if email is None or password is None:
        return Response({'error': 'Please provide both email and password'},
                        status=HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=email, password=password)

    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    user.last_login = timezone.now()
    user.save(update_fields=['last_login'])
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},status=HTTP_200_OK)


#! LISTING ALL MOVIES IN DB
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_movie(request):
    
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


#! SHOW MOVIE DETAILS
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def movie_detail(request, movie_id):
    
    movie = get_object_or_404(Movie, id=movie_id)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)

#! WATCH A MOVIE
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def watch_movie(request, movie_id):

    movie = get_object_or_404(Movie, id=movie_id)

    # Increment movie views
    movie.views = F('views') + 1
    movie.save()
    movie.refresh_from_db()

    # Add movie to watch history
    WatchHistory.objects.get_or_create(
        user=request.user,
        movie=movie
    )
    return Response({
        "message": "Movie started",
        "History": "Movie Added",
        "movie": movie.name,
        "views": movie.views
    })


#! ADD TO WATCH_LIST
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_watchlist(request, movie_id):

    movie = get_object_or_404(Movie, id=movie_id)
    watchlist, created = WatchList.objects.get_or_create(
        user=request.user,
        movie=movie
    )
    if created:
        return Response(
            {"message": "Successfully added to watchlist"},
            status=status.HTTP_201_CREATED
        )
    return Response(
        {"message": "Movie already exists in watchlist"},
        status=status.HTTP_200_OK
    )


#! SHOW WATCH_LIST
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_watchlist(request):
    watchlist = WatchList.objects.filter(user=request.user)
    serializer = WatchListSerializer(watchlist, many=True)
    return Response(serializer.data)


#! DELETE FROM WATCH_LIST
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_from_watchlist(request, movie_id):
    watchlist_item = get_object_or_404(WatchList, user=request.user, movie_id=movie_id)
    watchlist_item.delete()
    return Response(
        {"message": "Movie removed from watchlist"},
        status=status.HTTP_200_OK
    )


#! SHOW WATCH_HISTORY
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_watchhistory(request):
    watchhistory = WatchHistory.objects.filter(user=request.user).order_by("-watched_at")
    serializer = WatchHistorySerializer(watchhistory, many=True)
    return Response(serializer.data)


#! SEARCHING A MOVIE
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_movie(request):
    query = request.query_params.get("q")

    if not query:
        return Response({"error": "Valid search query is required"}, status=400)
    
    movies = Movie.objects.filter(name__icontains=query)
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


#! CAHNGE PASSWORD 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):

    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    if len(new_password) < 8:
        return Response(
            {"error": "Password must be at least 8 characters"},status=400)
    user = request.user

    if not user.check_password(old_password):
        return Response(
            {"error": "Current password is incorrect"},
            status=400
        )

    user.set_password(new_password)
    user.save()

    return Response(
        {"message": "Password changed successfully"},
        status=200
    )