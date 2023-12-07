from rest_framework import generics, permissions
from .models import Task
from .serializers import PostSerializer
from django.shortcuts import render, get_object_or_404

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

def post_list(request):
    posts = Task.objects.all()
    return render(request, 'post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Task, pk=pk)
    return render(request, 'post_detail.html', {'post': post})
