from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^users/$', views.UserListView.as_view(), name="user-list"),
    url(r'^user/(?P<pk>[0-9]+)/$', views.UserDetailView.as_view(), name="user-detail"),
    url(r'^login/$', views.LoginView.as_view(), name="login"),
    url(r'logout/$', views.LogoutView.as_view(), name="logout"),
]
