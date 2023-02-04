from django.urls import path
from textToSign.views import *

app_name= "textToSign"

urlpatterns=[
    path("text-to-signlanguage/",TextToSignView.as_view(),name="text"),
    path("signlanguage-to-text/",SignToTextView.as_view(),name="sign")
]