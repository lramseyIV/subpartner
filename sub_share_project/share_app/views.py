from django.shortcuts import render, redirect
from django.contrib import sessions, messages
from .models import Customer, Subscription
import bcrypt
# Create your views here.
def home(request):
    return render (request, 'index.html')

def login(request):
    if request.method=="GET":
        return render (request, 'login.html')
    if request.method=="POST":
        email = request.POST['email']
        password = request.POST['password']
        if not Customer.objects.filter(email=email):
            messages.error(request, 'email or password incorrect')
            return redirect ('/login')
        customer = Customer.objects.get(email=email)
        stored = customer.password
        if not bcrypt.checkpw(password.encode(), stored.encode()):
            messages.error(request, 'email or password incorrect')
            return redirect ('/login')
        request.session['id'] = customer.id
        return redirect ('/dashboard')

def register(request):
    if request.method=="GET":
        return render (request, 'register.html')
    if request.method=="POST":
        full_name = request.POST['full_name']
        email = request.POST['email']
        preferred_currency = request.POST['preferred_currency']
        password = request.POST['password']
        if Customer.objects.filter(email=email):
            messages.error(request, 'Email already exists.')
            return redirect('/register')
        if len(password) < 8:
            messages.error(request, 'Password MUST be 8 characters or more.')
            return redirect('/register')
        pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_customer = Customer.objects.create(full_name=full_name, email=email, preferred_currency=preferred_currency, password = pw)
        request.session['id'] = new_customer.id
        return redirect('/dashboard')

def logout(request):
    if 'id' not in request.session:
        return redirect ('/')
    del request.session['id']
    return redirect ('/')

def dashboard(request):
    if 'id' not in request.session:
        return redirect ('/')
    customer = Customer.objects.get(id=request.session['id'])
    context = {
        'customer': customer,
        # 'available_subs': Subscription.objects.filter(preferred_currency=customer.preferred_currency)
    }
    return render(request, 'dashboard.html', context)

def newsub(request):
    if request.method=="POST":
        if 'id' not in request.session:
            return redirect ('/')
        customer = Customer.objects.get(id=request.session['id'])
        name = request.POST['subscription_name']
        exp = request.POST['expiration']
        link = request.POST['group_link']
        cost = request.POST['cost']
        type = request.POST['type']
        slots = request.POST['slots']
        Subscription.objects.create(subscription_name=name, cost=cost, currency = customer.preferred_currency, expiration = exp, group_link=link, type=type, slots=slots, slots_available=slots, owner=customer)
        return redirect('/dashboard')
    
def delete(request, id):
    if 'id' not in request.session:
        return redirect ('/')
    customer = Customer.objects.get(id=request.session['id'])
    sub = Subscription.objects.get(id=id)
    if request.session['id'] != sub.id:
        return redirect ('/')
    sub.delete()
    return redirect('/dashboard')

def edit (request, id):
    if request.method=="GET":
        if 'id' not in request.session:
            return redirect ('/')
        customer = Customer.objects.get(id=request.session['id'])
        sub = Subscription.objects.get(id=id)
        if request.session['id'] != sub.owner.id:
            return redirect ('/')
        context = {
            'customer': customer,
            'sub': sub
        }
        return render (request, 'editsub.html', context)
    if request.method=="POST":
        if 'id' not in request.session:
            return redirect ('/')
        customer = Customer.objects.get(id=request.session['id'])
        sub = Subscription.objects.get(id=id)
        if request.session['id'] != sub.owner.id:
            return redirect ('/')
        name = request.POST['subscription_name']
        exp = request.POST['expiration']
        link = request.POST['group_link']
        cost = request.POST['cost']
        slots = request.POST['slots']
        taken = request.POST['taken'] 
        if int(slots) - int(taken) < 0:
            messages.error(request, 'Number of slots taken cannot exceed available.')
            return redirect (f'/edit/{id}')
        sub.subscription_name = name
        sub.expiration = exp
        sub.group_link = link
        sub.cost = cost
        sub.slots = slots
        sub.slots_taken = taken
        sub.slots_available = int(slots) - int(taken)
        sub.save()
        return redirect('/dashboard')
    
def change_currency(request):
    if request.method=="POST":
        if 'id' not in request.session:
            return redirect ('/')
    customer = Customer.objects.get(id=request.session['id'])
    curr = request.POST['preferred_currency']
    customer.preferred_currency = curr
    customer.save()
    messages.success(request, 'Currency Updated Successfully.')
    return redirect('/dashboard')


def edit_profile(request):
    if request.method=="GET":
        if 'id' not in request.session:
            return redirect ('/')
        customer = Customer.objects.get(id=request.session['id'])
        context = {
            'customer': customer,
        }
        return render(request, 'editprofile.html', context)
    if request.method=="POST":
        if 'id' not in request.session:
            return redirect ('/')
        customer = Customer.objects.get(id=request.session['id'])
        fn = request.POST['full_name']
        curr = request.POST['preferred_currency']
        if len(fn) < 3:
            messages.error(request, 'Name must be at least 3 characters')
            return redirect ('/editprofile')
        customer.full_name = fn
        customer.preferred_currency = curr
        customer.save()
        messages.success(request, 'Profile Information Updated')
        return redirect('/dashboard')

def change_password(request):
    if request.method=="POST":
        if 'id' not in request.session:
            return redirect ('/')
        customer = Customer.objects.get(id=request.session['id'])
        if not bcrypt.checkpw(request.POST['current_password'].encode(), customer.password.encode()):
            messages.error(request, 'Current Password incorrect')
            return redirect('/editprofile')
        if len(request.POST['new_password']) < 8:
            messages.error(request, 'New password MUST be at LEAST 8 characters long')
            return redirect('/editprofile')
        hashed = bcrypt.hashpw(request.POST['new_password'].encode(), bcrypt.gensalt()).decode()
        customer.password = hashed
        customer.save()
        messages.success(request, 'Password successfully updated')
        return redirect('/dashboard')


def market_view_preferred(request):
    if 'id' not in request.session:
        return redirect ('/')
    customer = Customer.objects.get(id=request.session['id'])
    context = {
        'subs': Subscription.objects.filter(currency=customer.preferred_currency).order_by('created_at').reverse(),
        'customer': customer
    }
    return render (request, 'market_preferred.html', context)

def market_all(request):
    if 'id' not in request.session:
        return redirect ('/')
    customer = Customer.objects.get(id=request.session['id'])
    context = {
        'subs': Subscription.objects.all().order_by('created_at').reverse(),
        'customer': customer
    }
    return render (request, 'market_all.html', context)

def report_scammer(request, email, m):
    if 'id' not in request.session:
        return redirect ('/')
    if not Customer.objects.filter(email=email):
        if m == 'p':
            return redirect('/market')
        else:
            return redirect('/marketall')
    scammer = Customer.objects.get(email=email)
    scammer.scammer_count += 1
    scammer.save()
    print(scammer.scammer_count)
    if m == 'p':
        return redirect('/market')
    else:
        return redirect('/marketall')