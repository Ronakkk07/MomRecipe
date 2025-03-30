from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import *
import uuid
from django.db.models import Q
# Create your views here.

@login_required(login_url='login')
def home(request):
    query = request.GET.get("query","")
    recipes = Recipe.objects.all().values("id", "title", "description", "image")
    
    if query is not None:
        recipes = Recipe.objects.filter(Q(title__icontains = query))
    else:
        recipes = Recipe.objects.all().values("id", "title", "description", "image")
    
    return render(request, 'home.html', {'recipes': recipes, 'query': query})

def add_recipe(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        image = request.FILES["image"]
        instructions = request.POST["instructions"]

        # Create and save the recipe
        Recipe.objects.create(
            id=uuid.uuid4(),
            title=title,
            description=description,
            image=image,
            instructions=instructions
        )
        return redirect("home")  # Redirect to home after submission

    return render(request, "add_recipe.html")

def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]


def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    if request.method == "POST":
        recipe.delete()
        return redirect('home')  # Redirect to the homepage or recipes list

    return redirect('recipe_detail', recipe_id=recipe.id)  # If accessed improperly       

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    comments = recipe.comments.all()  # Get all comments for this recipe

    if request.method == "POST":
        comment_text = request.POST.get('comment_text')  # Get input from HTML form
        if comment_text:
            Comment.objects.create(
                user=request.user,
                recipe=recipe,
                text=comment_text
            )
            return redirect('recipe_detail', recipe_id=recipe.id)  # Reload page
        
    return render(request, 'recipe_detail.html', {'recipe': recipe, 'comments': comments})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Ensure only the comment owner can delete
    if request.user == comment.user:
        comment.delete()
    
    return redirect('recipe_detail', recipe_id=comment.recipe.id)


def logout_view(request):
    logout(request)
    return redirect('login')