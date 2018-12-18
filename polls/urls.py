from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.LoginView.as_view(), name='login'),
    url(r'^login/', views.login, name='loginauth'),
    url(r'^register/', views.register, name='register'),
    url(r'^index/', views.IndexView.as_view(), name='index'),
    url(r'^history/', views.HistoryView.as_view(), name='history'),
    url(r'^serverhistory/', views.serverhistory, name='serverhistory'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
