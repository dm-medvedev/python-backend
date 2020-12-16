from django.urls import path
from django.contrib.auth.decorators import login_required

from papers.views import PaperView, paper_html_view, paper_view


urlpatterns = [
    path('', paper_view),
    path('all/', paper_html_view),
    path('api/', PaperView.as_view()),
]
