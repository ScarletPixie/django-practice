from django.http import JsonResponse
from django.middleware.csrf import get_token
from .models import Doc

def index(request):
    documents = list(Doc.objects.all().values())
    return JsonResponse({'documents': documents}, status=200)

def create(request):
    if request.method == 'GET':
        return JsonResponse({'csrf_token': get_token(request)})
    elif request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')

        if (title is None or text is None):
            return JsonResponse({'error': 'missing required fields', 'required_fields': ['title', 'text']}, status=400)

        try:
            document = Doc.object.create(title=title, text=text)
            document.save()
            return JsonResponse({'success': True, 'url': reverse('docs_app:detail', kwargs={'pk': document.pk})}, status=200)
        except Exception as e:
            return JsonResponse({'error': 'could not save document'}, status=400)

    return JsonResponse({'error': 'invalid request method'}, status=400)

def detail(request, pk):
    if request.method != 'GET':
        return JsonResponse({'error': 'invalid request method'}, status=400)

    doc = Doc.objects.get(pk=pk)
    if doc is None:
        return JsonResponse({'error': 'document not found'}, status=404)
    return JsonResponse({'title': doc.title, 'text': doc.text}, status=200)

