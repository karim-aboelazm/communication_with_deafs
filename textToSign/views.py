import cv2
import numpy as np
import tensorflow as tf
from keras.models import load_model
from django.shortcuts import render
from django.views.generic import TemplateView,FormView,CreateView
from django.views import View
from tensorflow.keras.preprocessing import image
from .forms import *
from .models import *

class TextToSignView(TemplateView):
    template_name="text_to_sign.html"
    def processInput(self,input_in_list):
        for s, i in enumerate(input_in_list):
            if "bye" in i.lower():
                input_in_list[s] = "static/img/bye.jpg"
            if "hello" in i.lower():
                input_in_list[s] = "static/img/hello.png"
            if "yes" in i.lower():
                input_in_list[s] = "static/img/yes.png"
            if "no" in i.lower():
                input_in_list[s] = "static/img/no.png"
            if "please" in i.lower():
                input_in_list[s] = "static/img/please.png"
            if "thanks" in i.lower():
                input_in_list[s] = "static/img/thanks.png"
            if "who" in i.lower():
                input_in_list[s] = "static/img/who.png"
            if "what" in i.lower():
                input_in_list[s] = "static/img/what.png"
            if "when" in i.lower():
                input_in_list[s] = "static/img/when.png"
            if "where" in i.lower():
                input_in_list[s] = "static/img/where.png"
            if "why" in i.lower():
                input_in_list[s] = "static/img/why.png"
            if "which" in i.lower():
                input_in_list[s] = "static/img/which.png"
            if "how" in i.lower():
                input_in_list[s] = "static/img/how.png"
        return input_in_list
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        input_text = self.request.GET.get("user_input")
        input_in_list = str(input_text).split(" ")
        context["same"]= self.processInput(input_in_list)
        context["og"]=input_text
        return context
    
class SignToTextView(FormView):
    template_name="sign_to_text.html"
    form_class = SignToTextForm
    model = SignToTextImage
    success_url = '/signlanguage-to-text/'
    
    
    def make_prediction(self,img):
        model = load_model('static/model.h5')
        classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 
               'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 
               'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 
               'u', 'v', 'w', 'x', 'y', 'z']
        img = image.load_img(img,target_size=(64,64))
        img = image.img_to_array(img)
        result = model.predict((np.expand_dims(img,axis=0)/255 - 0.5))[0] > 0.5
        return classes[result.tolist().index(True)]
    
    def form_valid(self, form):
        im = form.save(commit=False)
        image = form.cleaned_data['image']
        im.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        im = SignToTextImage.objects.latest('id')
        context["prediction"] = self.make_prediction(im.image.path)
        context["im"] = im
        context["numbers"] = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        return context

    