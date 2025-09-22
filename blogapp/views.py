from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, PostForm
from .models import Post


# User signup
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("post_list")
    else:
        form = SignUpForm()
    return render(request, "blogapp/signup.html", {"form": form})

# User login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("post_list")
    else:
        form = AuthenticationForm()
    return render(request, "blogapp/login.html", {"form": form})

# User logout
def logout_view(request):
    logout(request)
    return redirect("login")

# Show all posts
def post_list(request):
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "blogapp/post_list.html", {"posts": posts})

# Create post
@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("post_list")
    else:
        form = PostForm()
    return render(request, "blogapp/post_form.html", {"form": form})

# Update post
@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("post_list")
    else:
        form = PostForm(instance=post)
    return render(request, "blogapp/post_form.html", {"form": form})

# Delete post
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    post.delete()
    return redirect("post_list")

@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, "blogapp/my_posts.html", {"posts": posts})
