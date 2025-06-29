from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import Q
from contact.models import Contact
from django.core.paginator import Paginator
from contact.forms import ContactForm, RegisterForm, RegisterUpdateForm
from django.contrib import messages, auth
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.
def index(request):

    contacts = Contact.objects.all().filter(show=True).order_by('-id')
    pagination = Paginator(contacts, 10)


    page_number = request.GET.get('page')
    page_obj = pagination.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'site_title': 'Contatos - ',
    }
    

    return render(
        request,
        'contact/index.html',
        context,
    )

def contact(request, contact_id):

    single_contact = get_object_or_404(Contact, id=contact_id, show=True)

    context = {
        'contact': single_contact,
        'site_title': f'{single_contact.first_name} {single_contact.last_name} - '
    }

    return render(
        request,
        'contact/contact.html',
        context,
    )

def search(request):
    search_value = request.GET.get('q', '').strip()

    if search_value == '':
        return redirect('contact:index')

    contacts = Contact.objects.filter(show=True).filter(
        Q(first_name__icontains=search_value) | 
        Q(last_name__icontains=search_value) |
        Q(phone__icontains=search_value) |
        Q(email__icontains=search_value) |
        Q(first_name__icontains=search_value, last_name__icontains=search_value)
        )
    
    pagination = Paginator(contacts, 10)
    page_number = request.GET.get('page')
    page_obj = pagination.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'site_title': 'Contatos - ',
        'search_value': search_value,
    }
    

    return render(
        request,
        'contact/index.html',
        context,
    )


### Forms

non_permited = '!@#$%¨&*()-+"1234567890-=\|,.<>:}~^[]?/'


def create(request):
    form_action = reverse('contact:create')

    if request.method == 'POST':

        form = ContactForm(request.POST)

        context = {
            'form': form,
            'form_action': form_action,
            }

        if form.is_valid():
            contact = form.save()
            return redirect('contact:update', contact_id=contact.id)


        return render(
            request,
            'contact/create.html',
            context
            )       



    context = {
        'form': ContactForm(),
        'form_action': form_action,
    }

    return render(
        request,
        'contact/create.html',
        context
    )


def update(request, contact_id):

    contact_get = get_object_or_404(Contact, id=contact_id, show=True)
    form_action = reverse('contact:update', args=(contact_id, ))

    if request.method == 'POST':

        form = ContactForm(request.POST, instance=contact_get)

        context = {
            'form': form,
            'form_action': form_action,
            }

        if form.is_valid():
            contact = form.save()
            return redirect('contact:update', contact.id)


        return render(
            request,
            'contact/create.html',
            context
            )       


    context = {
        'form': ContactForm(instance=contact_get),
        'form_action': form_action,
    }

    return render(
        request,
        'contact/create.html',
        context
    )


def delete(request, contact_id):

    contact_get = get_object_or_404(Contact, id=contact_id, show=True)

    confirmation = request.POST.get('confirmation', 'no')

    if confirmation == 'yes':
        contact_get.delete()
        return redirect('contact:index')
    
    return render(
        request,
        'contact/contact.html',
        context={
            'contact': contact_get,
            'confirmation': confirmation,
        }
    )


def register(request):

    form = RegisterForm()

    if request.method == 'POST':

        form = RegisterForm(request.POST,)

        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário registrado')
            return redirect('contact:login')


    return render(
        request,
        'contact/register.html',
        {
            'form': form,
        }
    )


def login_view(request):

    form = AuthenticationForm(request)

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.success(request, f'Usuário logado com sucesso!')
            return redirect('contact:index')
        messages.error(request, 'Falha no login')


    return render(
        request,
        'contact/login.html',
        {
            'form': form
        }
    )

def logout_view(request):
    auth.logout(request)
    return redirect('contact:login')

    
def user_update(request):
    form = RegisterUpdateForm(instance=request.user)


    if request.method != 'POST':
        return render(
            request,
            'contact/register.html',
            context={
                'form': form
            }
        )


    form = RegisterUpdateForm(request.POST, instance=request.user)

    if not form.is_valid():
        return render(
            request,
            'contact/register.html',
            context={
                'form': form
            }
        )
    
    form.save()
    
    return redirect('contact:user_update')




