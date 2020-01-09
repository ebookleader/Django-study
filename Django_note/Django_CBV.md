# Django CBV (Class Based View)
## Index
1. Template Views with CBV
2. Detail View and List View
3. CRUD Views
---

1.Template Views with CBV
---------
**1. function based view VS template based view**
- function based view
```python
def index(request):
  return render(request, 'index.html')
```

- class based template view
```python
class IndexView(TemplateView):
  template_name = 'index.html' # template you want to return
```

**2. template view**
- urls.py
```python
from basic_app import views

urlpatterns = [
    ...,
    path('', views.IndexView.as_view()),
]
```
- views.py
```python
from django.views.generic import View, TemplateView

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['injectme'] = 'BASIC INJECTION!'
        return context
```
- index.html
```html
  ...
  {{ injectme }}
```



2.Detail View and List View
---------

3.CRUD Views
---------
