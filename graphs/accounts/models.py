from django.db import models
from django.contrib.auth.models import User
# Create your models here.

VIEWS =(
    ("ops","OPS"),
    ("noc","NOC"),
    ("telefonica","TELEFONICA"),
    ("correos","CORREOS"),
)

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE,related_name='profile')
    view = models.CharField(max_length=65535, choices=VIEWS, blank=True, null=True, verbose_name="Vistas")
    
    def __str__(self):
        return self.user.username


    def get_view(self):
        if self.view == 'noc' or self.view == 'ops':
            devices = {
                "172.20.237.90":[
                    {"1" : "CIEMAT-URJC-IMDEA NETWORK - F1 - (1)"},
                    {"2" : "CIEMAT-URJC-IMDEA NETWORK - F2 - (2)"},
                    {"3" : "Imdea Software F1 - (3)"},
                    {"4" : "Imdea Software F2 - (4)"},
                    {"5" : "UCM F1 - (5)"},
                    {"6" : "UCM F2 - (6)"},
                    {"7" : "CIB F1 - (7)"},
                    {"8" : "CIB F2 - (8)"},
                    {"9" : "UNED F1 - (9)"},
                    {"10" : "UNED F2 - (10)"},
                    {"11" : "Casa Velázquez F1 - (11)"},
                    {"12" : "Casa Velázquez F2 - (12)"},
                    {"13" : "UPM F1 - (13)"},
                    {"14" : "UPM F2 - (14)"},
                    {"15" : "UAM F1 - (15)"},
                    {"16" : "UAM F2 - (16)"}
                            
            ],
                "172.20.237.86":[
                    {"1" : "CSIC - UC3M - IMDEA NETWORK - F1 - (1)"},
                    {"2" : "CSIC - UC3M - IMDEA NETWORK - F2 - (2)"},
                    {"3" : "CSICJO F1 - (3)"},
                    {"4" : "CSICJO F2 - (4)"},
                    {"5" : "UCM F1 - (5)"},
                    {"6" : "UCM F2 - (6)"}
            ]  
            }
            fa = True
            return devices, fa
        if self.view == 'telefonica':
            # no puede hacer fault analysis
            devices = {
                "172.20.237.90":[
                    {"1" : "CIEMAT-URJC-IMDEA NETWORK - F1 - (1)"},
                    {"2" : "CIEMAT-URJC-IMDEA NETWORK - F2 - (2)"},
                    {"3" : "Imdea Software F1 - (3)"},
                    {"4" : "Imdea Software F2 - (4)"},
                    {"15" : "UAM F1 - (15)"},
                    {"16" : "UAM F2 - (16)"}
                            
            ],
                "172.20.237.86":[
                    {"1" : "CSIC - UC3M - IMDEA NETWORK - F1 - (1)"},
                    {"2" : "CSIC - UC3M - IMDEA NETWORK - F2 - (2)"},
                    {"3" : "CSICJO F1 - (3)"},
                    {"4" : "CSICJO F2 - (4)"},
            ]  
            }
            fa = True
            return devices, fa
        
        if self.view == 'correos':
            # no puede hacer fault analysis
            devices = {
                "172.20.237.86":[
                    {"5" : "UCM F1 - (5)"},
                    {"6" : "UCM F2 - (6)"}
            ]  
            }
            fa = False
            return devices, fa



