from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from .models import Movie, User, WatchHistory

# Create your views here.

def adminlogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return render(request, "login.html")
        user = authenticate(request,email=user_obj.email,password=password)
        if user and user.is_admin:
            login(request, user)
            return redirect("home")
        messages.error(request, "Invalid email or password")
    return render(request, "login.html")

@login_required(login_url='adminlogin')
def home(request):
    return render(request, 'home.html')


@login_required(login_url='adminlogin')
def addmovie(request):
    if request.method == "POST":
        try:
            movie_name = request.POST.get("movie_name")
            description = request.POST.get("description")
            release_year = request.POST.get("release_year")  # optional
            thumbnail = request.FILES.get("thumbnail")
            movie_file = request.FILES.get("movie_file")

            Movie.objects.create(
                name=movie_name,
                description=description,
                thumbnail=thumbnail,
                video=movie_file
            )
            messages.success(request, "Movie uploaded successfully!")
            return redirect("addmovie")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect("addmovie")
    return render(request, "addmovie.html")


@login_required(login_url='adminlogin')
def movielist(request):
    movies = Movie.objects.all().order_by('id')
    return render(request, 'movielist.html', {'movies': movies})


@login_required(login_url='adminlogin')
def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == "POST":
        movie.name = request.POST.get("movie_name")
        movie.description = request.POST.get("description")
        if request.FILES.get("thumbnail"):
            movie.thumbnail = request.FILES["thumbnail"]
        if request.FILES.get("video"):
            movie.video = request.FILES["video"]
        movie.save()
        messages.success(request, "Movie updated successfully.")
        return redirect("movielist")
    return render(
        request,
        "editmovie.html",
        {"movie": movie}
    )


@login_required(login_url='adminlogin')
def userlist(request):
    if not request.user.is_admin:
        return redirect('admin_login')
    users = User.objects.all().order_by('id')
    return render(request, 'userlist.html', {
        'users': users
    })


@login_required(login_url='adminlogin')
def blockuser(request, user_id):
    if not request.user.is_admin:
        return redirect('adminlogin')
    user = get_object_or_404(User, id=user_id)
    if not user.is_admin:  # prevent blocking admins
        user.is_active = False
        user.save()
    return redirect('userlist')


@login_required(login_url='adminlogin')
def unblockuser(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = True
    user.save()
    return redirect('userlist')


@login_required(login_url='adminlogin')
def user_history(request, user_id):

    user = get_object_or_404(User, id=user_id)
    history = WatchHistory.objects.filter(
        user=user
    ).select_related('movie').order_by('-watched_at')
    return render(
        request,
        'history.html',
        {
            'user_obj': user,
            'history': history
        }
    )



@login_required(login_url='adminlogin')
def reports(request):
    sort = request.GET.get('sort', 'views_desc')
    if sort == 'views_asc':
        movies = Movie.objects.all().order_by('views')
    elif sort == 'name_asc':
        movies = Movie.objects.all().order_by('name')
    elif sort == 'name_desc':
        movies = Movie.objects.all().order_by('-name')
    else:
        movies = Movie.objects.all().order_by('-views')
    return render(request,'reports.html',{'movies': movies,'selected_sort': sort})



@login_required(login_url='adminlogin')
def changepassword(request):
    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        user = request.user
        password_check = user.check_password(current_password)
        if not password_check:
            messages.error(request,"Current password is incorrect.")
            return render(request,"changepassword.html")
        passwords_match = (new_password == confirm_password)
        if not passwords_match:
            messages.error(request,"Passwords do not match.")
            return render(request,"changepassword.html")
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request,user)
        messages.success(request,"Password updated successfully.")
        return redirect("changepassword")

    return render(request,"changepassword.html")



@login_required(login_url='adminlogin')
def adminlogout(request):
    logout(request)
    return redirect("adminlogin")