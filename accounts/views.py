from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact
from django.contrib.auth.models import Group
from .forms import CustomAdminLoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from listings.models import Listing,Enquiry
from listings.forms import ListingForm
from realtors.models import Realtor
from django.contrib.auth.forms import UserCreationForm
from .forms import RealtorRegistrationForm
from django.db.models import Q


def customer_register(request):

    if request.method == 'POST':
        # register user
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # check if passwords match
        if password == password2:
            # Check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is taken.')
                return redirect('customer_register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email is being used.')
                    return redirect('customer_register')
                else:
                    # Validation looks good. Now register user.
                    user = User.objects.create_user(username=username, password=password,
                                                    email=email, first_name=first_name,
                                                    last_name=last_name)
                    # Login after registeration
                    # auth.login(request, user)
                    # messages.success(
                    #     request, 'You are successfully logged in.')
                    # return redirect('index')
                    user.save()
                    my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
                    my_customer_group[0].user_set.add(user)
                    messages.success(request, 'You are now registered.')
                    return redirect('customerlogin')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('customer_register')
    else:
        return render(request, 'accounts/customer_register.html')


def realtor_register(request):
    if request.method == 'POST':
        # register user
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # check if passwords match
        if password == password2:
            # Check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is taken.')
                return redirect('realtor_register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email is being used.')
                    return redirect('realtor_register')
                else:
                    # Validation looks good. Now register user.
                    user = User.objects.create_user(username=username, password=password,
                                                    email=email, first_name=first_name,
                                                    last_name=last_name)
                    # Login after registeration
                    # auth.login(request, user)
                    # messages.success(
                    #     request, 'You are successfully logged in.')
                    # return redirect('index')
                    user.save()
                    my_customer_group = Group.objects.get_or_create(name='REALTOR')
                    my_customer_group[0].user_set.add(user)
                    messages.success(request, 'You are now registered.')
                    return redirect('realtor_login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('realtor_register')
    else:
        return render(request, 'accounts/realtor_register.html')





def customerlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You successfully logged in.')
            return render(request, 'accounts/dashboard.html', {'customer':True })
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')



def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('index')


def dashboard(request):
    user_contacts = Contact.objects.order_by(
        '-contact_date').filter(user_id=request.user.id)

    context = {
        'contacts': user_contacts,
        'customer':True
    }
    return render(request, 'accounts/dashboard.html', context)

def realtor_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user:
            if user.groups.filter(name='REALTOR').exists():
                auth.login(request, user)
                messages.success(request, 'You successfully logged in')
                return redirect('realtor_dashboard')
            else:
                messages.error(request, 'You are not authorized as a Realtor')
                return redirect('realtor_login')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('realtor_login')

    return render(request, 'accounts/realtor_login.html')





#ADMIN 
def adminlogin(request):
    if request.method == 'POST':
        form = CustomAdminLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            return HttpResponse("Yay! you are human.")
        
        
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                 if user.is_superuser:
                    auth.login(request, user)
                    messages.success(request, 'You sucessfully logged in')
                    return redirect('admin_dashboard')                     
    admin_login_form=CustomAdminLoginForm()
    context={'admin_login_form':admin_login_form}
    return render(request, 'admin/adminlogin.html',context)

def admin_dashboard(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)
    # paginator = Paginator(listings, 6)
    context = {
        'listings': listings
    }
    return render(request, 'admin/admindashboard.html',context)


from django.db.models import Q  # Make sure this is imported

def managelistings(request):
    query = request.GET.get('q')  # Safely get the search term
    listings = Listing.objects.all().order_by('-list_date')

    if query:
        listings = listings.filter(
            Q(title__icontains=query) |
            Q(address__icontains=query) |
            Q(city__icontains=query) |
            Q(realtor__name__icontains=query) 
        )

    context = {
        'listings': listings
    }
    return render(request, 'admin/listings.html', context)


def managecontacts(request):
    user_contacts = Contact.objects.order_by(
        '-contact_date')

    # paginator = Paginator(listings, 6)
    context = {
        'contacts': user_contacts
    }
    return render(request, 'admin/contacts.html', context)

# def managerealtors(request):
#     properties = Property.objects.order_by('-listed_at')

#     # Paginator code can be added here if needed in the future
#     context = {
#         'properties': properties
#     }
#     return render(request, 'admin/realtor.html', context)

def managerealtors(request):
    query = request.GET.get('q')  # Safely get the search term
    realtors = Realtor.objects.all().order_by('-hire_date')

    if query:
        realtors = realtors.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query)  
        )
    # Paginator code can be added here if needed in the future
    context = {
        'realtors': realtors
    }
    return render(request, 'admin/realtor.html', context)



def addnew_realtor(request):
    if request.method == 'POST':
        
        user_form = UserCreationForm(request.POST)
        realtor_form = RealtorRegistrationForm(request.POST, request.FILES)
        if user_form.is_valid() and realtor_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])
            user.save()

            realtor = realtor_form.save(commit=False)
            realtor.user = user
            realtor.save()

            return redirect('managerealtors')  # redirect to a page showing the list of realtors
    else:
        user_form = UserCreationForm() 
    realtor_form = RealtorRegistrationForm()
    
    context = {
        'user_form': user_form,
        'form': realtor_form,
    }
    
    return render(request, 'admin/addnewrealtor.html', context)



def edit_listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, 'Listing updated successfully.')
            return redirect('managelistings')
    else:
        form = ListingForm(instance=listing)

    context = {
        'form': form,
        'listing': listing,
    }
    return render(request, 'admin/edit_listing.html', context)
from django.shortcuts import get_object_or_404

def delete_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    
    if request.method == 'POST':
        listing.delete()
        messages.success(request, 'Listing deleted successfully.')
        return redirect('managelistings')

    return render(request, 'admin/confirm_delete.html', {'listing': listing})

def edit_realtor(request, id):
    realtor = get_object_or_404(Realtor, id=id)
    if request.method == 'POST':
        realtor.name = request.POST.get('name')
        realtor.email = request.POST.get('email')
        realtor.phone = request.POST.get('phone')
        realtor.save()
        return redirect('managerealtors')
    return render(request, 'admin/edit_realtor.html', {'realtor': realtor})


def delete_realtor(request, id):
    realtor = get_object_or_404(Realtor, id=id)
    realtor.delete()
    return redirect('managerealtors')
    return render(request, 'admin/delete_realtor.html', {'realtor': realtor})


    
