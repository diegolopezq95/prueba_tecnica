from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Senior
from .serializers import SeniorSerializer
from rest_framework.decorators import api_view, permission_classes

from .forms import SeniorForm


def home(request):
    seniors = Senior.objects.all()
    return render(request, 'home.html', {'seniors': seniors})


@login_required
def new_greeting(request):
    seniors = Senior.objects.all()
    if request.method == 'POST':
        form = SeniorForm(request.POST)
        if form.is_valid():
            senior = form.save(commit=False)
            senior.created_by = request.user.username
            senior.save()
            """Senior.objects.create(
                greeting=form.cleaned_data.get('greeting'),
                position=form.cleaned_data.get('position'),
                name=form.cleaned_data.get('name'),
                created_by=request.user.username
            )"""
            return redirect('home')
    else:
        form = SeniorForm()
    return render(request, 'new_greeting.html', {'seniors': seniors, 'form': form})


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def greetings_get(request, pk):
    try:
        senior = Senior.objects.get(pk=pk)
    except Senior.DoesNotExist:
        return JsonResponse({'message': 'Greetings does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        senior_serializer = SeniorSerializer(senior)
        return JsonResponse(senior_serializer.data)
    elif request.method == 'PUT':
        senior_data = JSONParser().parse(request)
        senior_serializer = SeniorSerializer(senior, data=senior_data)
        if senior_serializer.is_valid():
            senior_serializer.save()
            return JsonResponse(senior_serializer.data)
        return JsonResponse(senior_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        senior.delete()
        return JsonResponse({'message': 'Greetings was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def greetings_post(request):
    if request.method == 'POST':
        senior_data = JSONParser().parse(request)
        senior_serializer = SeniorSerializer(data=senior_data)
        if senior_serializer.is_valid():
            senior_serializer.save()
            return JsonResponse(senior_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(senior_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
