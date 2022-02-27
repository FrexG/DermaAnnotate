from django.urls import path

from .views import Index,Login,Logout

app_name = "annotate"

urlpatterns = [
    path("index",Index.as_view(),name="index"),
    path("",Login.as_view(),name="login"),
    path("logout",Logout.as_view(),name="logout"),

]

