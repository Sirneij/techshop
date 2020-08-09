from django.shortcuts import render

def handler404(request):
    page_title = 'Page Not Found'
    return render(request,"404.html", locals(), status=404)

def handler500(request):
    return render(request,'500.html', locals(), status=500)

def app_offline(request):
    page_title = 'Application is offline'
    return render(request, 'app_offline.html', locals())
