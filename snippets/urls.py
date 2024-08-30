from django.urls import path

from .views import SnippetView, SnippetViewV2, SnippetDetail

urlpatterns = [
    path('snippets/v2/<int:pk>/', SnippetDetail.as_view()),
    path('snippets/v2/', SnippetViewV2.as_view(), name='get_snippets'),
    path('snippets/', SnippetView.as_view(), name='get_snippets'),
    path('snippets/<int:id>/', SnippetView.as_view(), name='update_snippets'),
]
