from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate,login,logout
# import models
from .models import Dataset,Annotation
# Create your views here.
class Login(View):
    template_name = "DermaAnnotate/login.html"
    def get(self,request):
        return render(request,template_name=self.template_name)

    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        authenticate_user = authenticate(request,username = username,password = password)

        if authenticate_user is not None:
            login(request,authenticate_user)
            return redirect("annotate:index")
        else:
            messages.info(request,"Incorrect Credentials")
            return redirect("annotate:login")
class Logout(View):
    def get(self,request):
        logout(request)
        return redirect("annotate:login")


class Index(LoginRequiredMixin,View):
    data = None
    def get(self,request):
        labels = Annotation.objects.filter(labeled_by = request.user).order_by("id").last()
        label_count = Annotation.objects.filter(labeled_by = request.user).count()
        total_images = Dataset.objects.all().count()

        if labels:  # if the query is not  empty
            context = {"data":Dataset.objects.get(pk = labels.image.id + 1),"label_count":label_count + 1,"image_count":total_images}
            
        else:
            self.data = Dataset.objects.order_by("id").first()
            context = {"data":self.data,"label_count":1,"image_count":total_images}
        #return HttpResponse("Hello, This is test")
        return render(request,'DermaAnnotate/index.html',context)

    def post(self,request):
        assigned_label = request.POST["annotation"]
        
        labels = Annotation.objects.filter(labeled_by = request.user).order_by("id").last()

        if labels:  # if the query is not  empty
            self.data = Dataset.objects.get(pk = labels.image.id + 1)
            
        else:
            self.data = Dataset.objects.order_by("id").first()
        
        print(f"========> {self.data.image_path}")
        annot = Annotation(image = self.data,labeled_by = request.user,label = assigned_label)
        annot.save()

        return redirect("annotate:index")

