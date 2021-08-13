import time
import re
from django_currentuser.middleware import get_current_user, get_current_authenticated_user
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import IntegrityError
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from auctions.models import *
from django import forms
from django.forms import ModelForm
from django.contrib.sessions.models import Session


class ALListView(ListView):
    model = AL
    template_name= 'auctions/index.html'
    context_object_name = 'al'
    ordering = ['-timestamp']


    
    
    
class ALDetailView(LoginRequiredMixin,DetailView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    model = AL

    
    
    
    def get_context_data(self,  *args, **kwargs):
        context = super(ALDetailView, self).get_context_data( *args, **kwargs)
        x = kwargs.get('pk')
        al = AL.objects.all()
        
        auctions= self.get_object()
        
        self.request.user == auctions.username
        context['b']  = Bid.objects.filter(y=auctions.id).order_by('-current_bid')
        context['a']  = Comment.objects.all().order_by('-timestamp')
    
        
        return context 
        
    
    
def com(request):
     
        if request.method == "POST":
            comment= request.POST.get("comment")
            
            k = request.POST.get("ky")
            
            c = Comment(comment=comment, username= request.user, i=k)
            c.save()
            return HttpResponseRedirect(reverse("al_detail", args =[k] ))
        else:
            return HttpResponseRedirect("")


def bidder(request):
    if request.method == "POST":
        k1 = request.POST.get("kyy")
        current_bid = int(request.POST.get("bid"))
        b1 = Bid.objects.filter(y=k1)
        if not b1:
            #check if currentbid is greater than current price
            auctions= AL.objects.get(id=k1)
            if current_bid > auctions.current_price:
                b2 = Bid(current_bid=current_bid, username= request.user, y=k1)
                b2.save()
                return HttpResponseRedirect(reverse("al_detail", args =[k1] ))
            else:
                
                return HttpResponseRedirect(reverse("al_detail", args =[k1] ))
        else:
                bz = list(b1.filter(y=k1).order_by('-current_bid')) 
                
                if current_bid > bz[0].current_bid:
                    b2 = Bid(current_bid=current_bid, username= request.user, y=k1)
                    b2.save()
                    return HttpResponseRedirect(reverse("al_detail", args =[k1] ))
                else:
                    return HttpResponseRedirect(reverse("al_detail", args =[k1] ))
    else:
        return HttpResponseRedirect("")

    
 


   
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
       
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")






@login_required(login_url='login')
def categories(request):
    auc = AL.objects.values('category').distinct()
    
    return render(request, "auctions/categories.html",{"auc" : auc} )


class ALCreateView(LoginRequiredMixin, CreateView):
    model = AL
    fields = ['current_price', 'img', 'title', 'category', 'contacts', 'description']
    
    def form_valid(self, form):
        form.instance.username= self.request.user
        return super().form_valid(form)



class ALDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = AL
    
    success_url = "/"
    
    def test_func(self):
        auctions= self.get_object()
        

        if self.request.user == auctions.username:
        
            
            return True
        return False
       


       
    
def cat(request, **kwargs):
        x= kwargs.get('category')
        ab = AL.objects.filter(category = str(x))
        return render(request, "auctions/index.html", { "ab" : ab } )

       
@login_required(login_url='login')
def watchlist(request, id):
    fav = bool
    al = get_object_or_404(AL, id=id)
    if al.favourites.filter(id = request.user.id).exists():
        
        al.favourites.remove(request.user)
        
        
    else:
        al.favourites.add(request.user)
        
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
    

@login_required(login_url='login')
def watch_list(request):
    new = AL.objects.filter(favourites=request.user)
    
    
    return render(request, "auctions/watchlist.html" ,{"new":new})


@login_required(login_url='login')
def closed_auctions(request, **kwargs):
    cb = Close_Bid.objects.all().order_by('-current_bid')
  
    return render(request, "auctions/closed_auctions.html" ,{"cb":cb})



def delete(request, **kwargs):
    if request.method == "POST":
        de = request.POST.get("de")
    al = AL.objects.get(id = de)
    bid = Bid.objects.filter(y=de).order_by('-current_bid').first()
    if bid ==None:
        y = Close_Bid(username= al.username, current_bid = al.current_price, y = al.id,  img= al.img, title= al.title, io= True)
        y.save()
    else:
        y = Close_Bid(username= bid.username, current_bid = bid.current_bid, y = bid.y,  img= al.img, title= al.title, io= True)
        y.save()
        
   
        
    b= Bid.objects.filter(y=de)
    b.delete()
    al = AL.objects.filter(id = de)
    al.delete()
    al = AL.objects.all().order_by('-timestamp')
    return render(request, "auctions/index.html" ,{"al":al})