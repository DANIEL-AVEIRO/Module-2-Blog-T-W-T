from django.shortcuts import render, redirect
from app.models import PostModel, CategoryModel, CommentModel
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.


def index(request):
    search = request.GET.get("search")
    posts = PostModel.objects.all().order_by("-created_at")
    if search:
        posts = posts.filter(
            Q(title__icontains=search)
            | Q(description__icontains=search)
            | Q(category__name__icontains=search)
        )
    else:
        posts = posts
    return render(request, "index.html", {"posts": posts, "search": search})


def post_list(request):
    posts = PostModel.objects.all()
    return render(request, "post_list.html", {"posts": posts})


def post_create(request):
    categories = CategoryModel.objects.all()
    if request.method == "GET":
        return render(request, "post_create.html", {"categories": categories})  # <=
    if request.method == "POST":
        title = request.POST.get("title")
        viewer = request.POST.get("viewer")
        description = request.POST.get("description")
        image = request.FILES.get("image")
        category = request.POST.get("category")  # ဒါလေးရယ်

        post = PostModel.objects.create(
            title=title,
            description=description,
            viewer=viewer,
            image=image,
            category_id=category,  # ဒါလေးရယ်
        )
        post.save()
        return redirect("/post/list/")


def post_update(request, pk):
    categories = CategoryModel.objects.all()
    post = PostModel.objects.get(id=pk)
    if request.method == "GET":
        return render(
            request, "post_update.html", {"post": post, "categories": categories}
        )
    if request.method == "POST":
        title = request.POST.get("title")
        viewer = request.POST.get("viewer")
        description = request.POST.get("description")
        image = request.FILES.get("image")
        category = request.POST.get("category")

        post.title = title
        post.description = description
        post.viewer = viewer
        post.category_id = category
        if image:
            if post.image:
                post.image.delete()
            post.image = image
        post.save()
        return redirect("/post/list/")


def post_delete(request, pk):
    post = PostModel.objects.get(id=pk)
    if request.method == "GET":
        return render(request, "post_delete.html", {"post": post})
    if request.method == "POST":
        if post.image:
            post.image.delete()
        post.delete()
        return redirect("/post/list/")


def post_details(request, pk):
    post = PostModel.objects.get(id=pk)
    comments = CommentModel.objects.filter(post_id=post.id).order_by("-created_at")
    return render(request, "post_details.html", {"post": post, "comments": comments})


def category_list(request):
    categories = CategoryModel.objects.all()
    return render(request, "category_list.html", {"categories": categories})


def category_create(request):
    if request.method == "GET":
        return render(request, "category_create.html")
    if request.method == "POST":
        name = request.POST.get("name")

        category = CategoryModel.objects.create(name=name)
        category.save()
        return redirect("/category/list/")


def category_update(request, pk):
    category = CategoryModel.objects.get(id=pk)
    if request.method == "GET":
        return render(request, "category_update.html", {"category": category})
    if request.method == "POST":
        name = request.POST.get("name")
        category.name = name
        category.save()
        return redirect("/category/list/")


def category_delete(request, pk):
    category = CategoryModel.objects.get(id=pk)
    if request.method == "GET":
        return render(request, "category_delete.html", {"category": category})
    if request.method == "POST":
        category.delete()
        return redirect("/category/list/")


def login_view(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("/")
        return render(request, "login.html")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        # if user is not None:
        if user:
            login(request, user)
            messages.success(request, "Login successfully")
            return redirect("/")
        else:
            messages.warning(request, "Invalid credential")
            return redirect("/login/")


def logout_view(request):
    logout(request)
    return redirect("/login/")


def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        existing_username = User.objects.filter(username=username).exists()

        if existing_username:
            messages.warning(request, "username already exists")
            return redirect("/register/")

        if password != confirm_password:
            messages.error(request, "Password does not match")
            return redirect("/register/")

        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        user.save()
        # login(request, user)
        messages.success(request, f"Account create successfully {user.username}")
        return redirect("/login/")


def comment_create(request, post_id):
    post = PostModel.objects.get(id=post_id)
    if request.method == "POST":
        comment = CommentModel.objects.create(
            post_id=post.id,
            author_id=request.user.id,
            message=request.POST.get("message"),
        )
        comment.save()
        messages.success(request, "Comment successfully")
        return redirect(f"/post/details/{post.id}/")
