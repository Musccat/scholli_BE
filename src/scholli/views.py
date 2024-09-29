from django.shortcuts import render, redirect

def main(request):
    if not request.user.is_authenticated:
        return render(request, "main_before.html")
    else:
        return render(request, "main_after.html")
