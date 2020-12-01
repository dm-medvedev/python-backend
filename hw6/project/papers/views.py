from django.http import Http404, HttpResponse
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Paper
from .serializers import PaperSerializer


def paper_view(request):
    return HttpResponse("Welcome to papers you can visit "
                        "`papers/all` and `papers/api`!")


def paper_html_view(request):
    papers = Paper.objects.all()
    return render(request, 'base.html',
                  {'title': 'Available papers', 'papers': papers})


def filter_request(request):
    papers = Paper.objects.all()
    dict_ = request.query_params
    kwargs = {f"{field.name}__icontains": dict_.get(field.name, None)
              for field in Paper._meta.fields}
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    papers = [] if len(kwargs) == 0 else papers.filter(**kwargs)
    return papers


class PaperView(APIView):
    def get(self, request):
        try:
            papers = filter_request(request)
            serializer = PaperSerializer(papers, many=True)
        except:
            raise Http404
        return Response({'get': serializer.data})

    def post(self, request):
        if request.POST.get('id', None) is None:
            raise Http404('you have to pass `id`')
        try:
            to_change = {k: v for k, v in request.POST.items() if k != 'id'}
            obj = Paper.objects.filter(pk=request.POST['id'])
            obj.update(**to_change)
            return Response({'post': f"{request.POST['id']} updated"})
        except:
            raise Http404

    def put(self, request):
        try:
            Paper.objects.create(**{k: v for k, v in request.POST.items()})
            return Response({'put': 'success'})
        except:
            raise Http404

    def delete(self, request):
        try:
            papers = filter_request(request)
            print(papers)
            papers.delete()
            return Response({'delete': 'success'})
        except:
            raise Http404
