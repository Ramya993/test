
from django.conf.urls import include, url
from  .views  import  Hello,IdealWeight,getservices,insertservices,updateservices,deleteservices
urlpatterns = [
    
        url(r'^hello',Hello,name='Hello'),  
        url(r'^idealweight',IdealWeight),
        url(r'^getservices',getservices),
        url(r'^insertservices',insertservices),       
        url(r'^updateservices/(?P<ServiceId>\d+)$',updateservices),
        url(r'^deleteservices/(?P<ServiceId>\d+)$',deleteservices),
]