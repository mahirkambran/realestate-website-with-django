from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from .choices import bedroom_choices, state_choices, price_choices
from .models import Listing, Enquiry, Realtor
from .forms import ListingForm
from django.contrib import messages

def index(request):
    # All published listings (paginated)
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)

    # Featured listings for carousel (top 5 latest)
    featured_listings = Listing.objects.filter(is_published=True).order_by('-list_date')[:5]

    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    
   

    context = {
        'listings': paged_listings,       # for grid
        'featured_listings': featured_listings,  # for hero carousel
        'customer': True,
    }

    # 👉 Render to homepage
    return render(request, 'listings/listings.html', context)


def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    return render(request, 'listings/listing.html', {'listing': listing})


def search(request):
    queryset_list = Listing.objects.order_by('-list_date')

    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']

        if keywords:
            queryset_list = queryset_list.filter(
                description__icontains=keywords)

    # City
    if 'city' in request.GET:
        city = request.GET['city']

        if city:
            queryset_list = queryset_list.filter(
                city__iexact=city)

    # City
    if 'state' in request.GET:
        state = request.GET['state']

        if state:
            queryset_list = queryset_list.filter(
                state__iexact=state)

    # Bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']

        if bedrooms:
            queryset_list = queryset_list.filter(
                bedrooms__iexact=bedrooms)

    # Price
    if 'price' in request.GET:
        price = request.GET['price']

        if price:
            queryset_list = queryset_list.filter(
                price__lte=price)

    context = {
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings': queryset_list,
        'values': request.GET
    }
    return render(request, 'listings/search.html', context)


def add_property(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('managelistings')
    else:
        form = ListingForm()
    return render(request, 'listings/add_property.html', {'form': form})

def enquiry_form(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    realtor = listing.realtor 
    context = {
        'listing': listing,
        'realtor': realtor,
    }
    if request.method == 'POST':
        message = request.POST.get('message')        
        listing = get_object_or_404(Listing, pk=listing_id)
        realtor = listing.realtor 
        customer = request.user  
        # Save enquiry to DB
        enquiry = Enquiry(
            listing=listing,
            customer=customer,
            realtor=realtor,
            message=message
        )
        enquiry.save()

        messages.success(request, 'Your enquiry has been submitted.')
        return redirect('/')   
   
    return render(request, 'listings/enquiry.html')

def enquiry_list_view(request):
    enquiries = Enquiry.objects.all().order_by('-contact_date')
    return render(request, 'admin/enquiry_view.html', {'enquiries': enquiries})