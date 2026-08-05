from django.db import models
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import Book, Commande, CommandeBooks, Panier, User
from .forms import AddressForm


# Create your views here.
def home(request):
    featured_books = Book.objects.all()[:4]
    context = {
        'featured_books': featured_books,
        'books_count': Book.objects.count(),
    }
    return render(request, 'acceuil.html', context)


def shop(request):
    query = request.GET.get('q', '')
    if query:
        books = Book.objects.filter(
            models.Q(title__icontains=query) | models.Q(author__icontains=query)
        )
    else:
        books = Book.objects.all()
    context = {
        'books': books,
        'books_count': books.count(),
        'query': query,
    }
    return render(request, 'shopi/shop.html', context)


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'shopi/book_detail.html', {'book': book})


@login_required(login_url='login')
def panier(request, id):
    if request.user.id != id:
        return redirect('panier', id=request.user.id)

    user = request.user
    panier_items = Panier.objects.filter(user=user).select_related('book')
    context = {
        'user': user,
        'panier_items': panier_items,
    }
    return render(request, 'shopi/panier.html', context)


@login_required(login_url='login')
def commande(request,id):
    if request.user.id != id:
        return redirect('commande', id=request.user.id)

    user = request.user
    commandes = Commande.objects.filter(user=user)
    usercommandes = CommandeBooks.objects.filter(commande__in=commandes).select_related('book', 'commande')

    context = {
        'user': user,
        'commandes': usercommandes,
    }

    return render(request, 'shopi/commande.html', context)



def login(request):
    if request.user.is_authenticated:
        return redirect('shop')

    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('shop')

        context = {
            'username': username,
            'error': "Incorrect username or password.",
        }

    return render(request, 'login.html', context)

def logout(request):
    # Logic for handling logout
    auth.logout(request)
    return redirect('login')

def register(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        address = request.POST.get('address', '').strip()
        code_postal = request.POST.get('code_postal', '').strip()
        context = {
            'email': email,
            'username': username,
            'address': address,
            'code_postal': code_postal,
        }

        if password != confirm_password:
            context['error'] = "Passwords do not match."
            return render(request, 'register.html', context)

        if User.objects.filter(username=username).exists():
            context['error'] = "Username already exists."
            return render(request, 'register.html', context)

        user = User.objects.create_user(username=username, email=email, password=password)
        user.address = address
        user.code_postal = code_postal
        user.save()
        auth.login(request, user)
        return redirect('shop')

    return render(request, 'register.html', context)

@login_required(login_url='login')
def ajouter_au_panier(request, item_id):
    book = get_object_or_404(Book, id=item_id)
    panier_item, created = Panier.objects.get_or_create(user=request.user, book=book)
    if not created:
        panier_item.quantity += 1
        panier_item.save(update_fields=['quantity'])

    return redirect('panier', id=request.user.id)

@login_required(login_url='login')
def adresse(request, item_id):
    panier_item = get_object_or_404(
        Panier.objects.select_related('book'),
        id=item_id,
        user=request.user,
    )

    if request.method == 'POST':
        commande = Commande.objects.create(
            user=request.user,
            adresse=request.user.address,
        )
        CommandeBooks.objects.create(
            commande=commande,
            book=panier_item.book,
            quantity=panier_item.quantity,
        )
        panier_item.delete()
        return redirect('commande', id=request.user.id)

    context = {
        'panier_item': panier_item,
    }
    return render(request, 'shopi/adresse.html', context)

@login_required(login_url='login')
def supprimer_du_panier(request, item_id):
    panier_item = get_object_or_404(
        Panier,
        id=item_id,
        user=request.user,
    )
    panier_item.delete()
    return redirect('panier', id=request.user.id)


@login_required(login_url='login')
def pass_commande(request, item_id):
    return redirect('adresse', item_id=item_id)


@login_required(login_url='login')
def saved_addresses(request):
    context = {
        'user': request.user,
    }
    return render(request, 'shopi/saved_addresses.html', context)


@login_required(login_url='login')
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            user = request.user
            user.address = form.cleaned_data['address']
            user.code_postal = form.cleaned_data['code_postal']
            user.phone_number = form.cleaned_data['phone_number']
            user.save()
            return redirect('saved_addresses')
    else:
        form = AddressForm()
    return render(request, 'shopi/address_form.html', {'form': form, 'title': 'Add Address'})


@login_required(login_url='login')
def edit_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('saved_addresses')
    else:
        form = AddressForm(instance=request.user)
    return render(request, 'shopi/address_form.html', {'form': form, 'title': 'Edit Address'})


@login_required(login_url='login')
def delete_address(request):
    user = request.user
    user.address = ''
    user.code_postal = ''
    user.phone_number = ''
    user.save()
    return redirect('saved_addresses')


@login_required(login_url='login')
def order_history(request):
    commandes = Commande.objects.filter(user=request.user).order_by('-date_commande')
    commande_items = CommandeBooks.objects.filter(commande__in=commandes).select_related('book', 'commande')
    context = {
        'commandes': commandes,
        'commande_items': commande_items,
    }
    return render(request, 'shopi/order_history.html', context)


def authors(request):
    authors = Book.objects.values_list('author', flat=True).distinct()
    context = {
        'authors': authors,
    }
    return render(request, 'shopi/authors.html', context)


def author_books(request, author_name):
    books = Book.objects.filter(author=author_name)
    context = {
        'author_name': author_name,
        'books': books,
    }
    return render(request, 'shopi/author_books.html', context)


@login_required(login_url='login')
def supprimer_du_commande(request, item_id):
    commande_item = get_object_or_404(
        CommandeBooks.objects.select_related('commande'),
        id=item_id,
        commande__user=request.user,
    )
    commande = commande_item.commande
    commande_item.delete()

    if not CommandeBooks.objects.filter(commande=commande).exists():
        commande.delete()

    return redirect('commande', id=request.user.id)
