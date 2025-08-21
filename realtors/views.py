from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RealtorForm,RealtorLoginForm
from .models import Realtor
from listings.models import Enquiry
from .forms import PropertyForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import get_object_or_404


# @login_required
def realtor_register(request):
    if request.method == 'POST':
        realtor_form = RealtorForm(request.POST, request.FILES)
        user_form = UserCreationForm(request.POST)
        # print(form)
        if user_form.is_valid():
            # print("ratheesh")
            user = user_form.save()
            realtor=realtor_form.save(commit=False)
            realtor.user=user
            realtor.save()
            # print("ratheesh")
              # Add user to REALTOR group
            realtor_group = Group.objects.get(name='REALTOR')
            user.groups.add(realtor_group)
            return redirect('realtor_login')
    else:
        realtor_form = RealtorForm()
        user_form = UserCreationForm()   
    return render(request, 'accounts/realtor_form.html', {'form': realtor_form,'user_form':user_form})

def realtor_login(request):
    form = RealtorLoginForm(request.POST or None)  
    
    if request.method == 'POST':
        if form.is_valid(): 
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            
            if user:
                if user.groups.filter(name='REALTOR').exists():
                    login(request, user)
                    messages.success(request, 'You successfully logged in')
                    return render(request, 'accounts/realtor_dashboard.html', {
                        'realtor': 'realtor'
                    })
                else:
                    messages.error(request, 'You are not authorized as a Realtor')
                    return redirect('realtor_login')
            else:
                messages.error(request, 'Invalid credentials')
                return redirect('realtor_login')

    return render(request, 'accounts/realtor_login.html', {'realtor_login_form': form})

def realtor_dashboard(request):
    # Get the Realtor object associated with the logged-in user
    realtor = get_object_or_404(Realtor, user=request.user)
    
    # Filter enquiries for that realtor
    enquiries = Enquiry.objects.filter(realtor=realtor.id).order_by('-contact_date')
    

    return render(request, 'accounts/realtor_dashboard.html', {
        'enquiries': enquiries
    })
    
def approve_enquiry(request, enquiry_id):
    enquiry = get_object_or_404(Enquiry, id=enquiry_id, realtor=request.user)
    enquiry.is_approved = True
    enquiry.save()
    messages.success(request, 'Enquiry approved successfully.')
    return redirect('realtor_dashboard')

def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            form.save()
            return redirect('listings')  # Redirect to a property list view or another page after saving
    else:
        form = PropertyForm()
    return render(request, 'add_property.html', {'form': form})

