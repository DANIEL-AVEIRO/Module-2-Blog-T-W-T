from django.shortcuts import render, redirect
from app.models import PostModel, CategoryModel

# Create your views here.


def index(request):
    return render(request, "index.html")


def post_list(request):
    posts = PostModel.objects.all()
    return render(request, "post_list.html", {"posts": posts})


def post_create(request):
    categories = CategoryModel.objects.all()  # <=
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
