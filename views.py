from django.urls import path
from .views import CompanyListView, CompanyDetailView, CompanyCreateView, CompanyUpdateView, CompanyDeleteView
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Company
from .serializers import CompanySerializer
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.urls import path
from .views import CompanyListView, CompanyDetailView, CompanyCreateView, CompanyUpdateView, CompanyDeleteView
from .views import DocListView, DocDetailView, DocCreateView, DocUpdateView, DocDeleteView, DocSignView
from .views import UserListView, UserDetailView, UserCreateView, UserUpdateView, UserDeleteView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Company, Doc, User
from .forms import CompanyForm, DocForm, UserForm
from django.shortcuts import redirect, get_object_or_404
from .models import Company, Doc, User

def edit_document(request, id):
    doc = get_object_or_404(Doc, pk=id)
    if request.method == 'POST':
        form = DocForm(request.POST, instance=doc)
        if form.is_valid():
            form.save()
            return redirect('doc_list')
    else:
        form = DocForm(instance=doc)
    return render(request, 'edit_document.html', {'form': form})

urlpatterns = [
    # ... outras URLs ...
    path('doc/delete/<int:id>/', views.delete_document, name='delete_document'),
]


def delete_document(request, id):
    doc = get_object_or_404(Doc, pk=id)
    doc.delete()
    return redirect('doc_list')


def update_document(request, id):
    doc = get_object_or_404(Doc, pk=id)
    form = DocForm(request.POST or None, instance=doc)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('doc_list')
    return render(request, 'update_document.html', {'form': form})


urlpatterns = [
    path('companies/', CompanyListView.as_view(), name='company-list'),
    path('companies/create/', CompanyCreateView.as_view(), name='company-create'),
    path('companies/<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),
    path('companies/<int:pk>/update/', CompanyUpdateView.as_view(), name='company-update'),
    path('companies/<int:pk>/delete/', CompanyDeleteView.as_view(), name='company-delete'),
    
    path('docs/', DocListView.as_view(), name='doc-list'),
    path('docs/create/', DocCreateView.as_view(), name='doc-create'),
    path('docs/<int:pk>/', DocDetailView.as_view(), name='doc-detail'),
    path('docs/<int:pk>/update/', DocUpdateView.as_view(), name='doc-update'),
    path('docs/<int:pk>/delete/', DocDeleteView.as_view(), name='doc-delete'),
    path('docs/<int:pk>/sign/', DocSignView.as_view(), name='doc-sign'),
    
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/create/', UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
]


urlpatterns = [
    path('companies/', views.CompanyList.as_view()),
    path('companies/<int:pk>/', views.CompanyDetail.as_view()),
    path('docs/', views.DocList.as_view()),
    path('docs/<int:pk>/', views.DocDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)


@api_view(['GET', 'POST'])
def company_list(request):
    if request.method == 'GET':
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CompanySerializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk)

    if request.method == 'GET':
        serializer = CompanySerializer(company)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CompanySerializer(company, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
