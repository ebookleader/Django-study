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
```python
from django.views.generic import View, TemplateView, ListView, DetailView
```
**1. list view**
```python
class SchoolListView(ListView):
    # If you don't pass in this attribute, 
    # Django will auto create a context name for you with object_list!
    # Default would be 'school_list'

    # Example of making your own:
    context_object_name = 'schools'
    
    model = models.School
```
**2. detail view**
```python
class SchoolDetailView(DetailView):
    context_object_name = 'school_detail'
    model = models.School
    #in defaul, django return school(lowercase)
```

- models
```python
class School(models.Model):
  ...
  # if you didn't indicate the primary field,
  # in background django set an id for every entry which is numeric indicator
```
```python
class Student(models.Model):
  ...
 school = models.ForeignKey(School, related_name='students', on_delete=models.CASCADE)
```
- school.id is a primary key of School 
```html
{% for school in schools %}
    <h2><li><a href="{{school.id}}">{{school.name}}</a></li></h2>
{% endfor %}
```
- `<`int:pk`>`
```python
path('<int:pk>/',views.SchoolDetailView.as_view(), name='detail')
# in this case, pk is school.id
```
- school_detail.students.all
```html
{% for student in school_detail.students.all %}
  <!--students is related_name in model-->
  <p>{{student.name}} who is {{student.age}} years old</p>
{% endfor %}
```

3.CRUD Views
---------
**C**reate **R**etrieve **U**pdate **D**elete
```python
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
```
- CBVs have template names they automatically look for (which is something you can overwrite with the template_name attribute)<br>
-> school_form.html, school_confirm_delete.html, school_list.html etc.
- Example
```html
    {% if not form.instance.pk %}
    Create School
    {% else %}
    Update School
    {% endif %}
```
- urls.py
```python
  ...
  path('create/', views.SchoolCreateView.as_view(), name='create'),
  path('update/<int:pk>/', views.SchoolUpdateView.as_view(), name='update'),
  path('delete/<int:pk>/', views.SchoolDeleteView.as_view(), name='delete'),
```

1.Create
```python
class SchoolCreateView(CreateView):
    fields = # clarify fields you want to create
    model = # connect model
```
2.Update
```python
class SchoolUpdateView(UpdateView):
    fields = # clarify fields you want to update
    model = # connect model
```
```html
<a href="{% url 'basic_app:update' pk=school_detail.pk %}">Update</a>
```
3.Delete
```python
class SchoolDeleteView(DeleteView):
    model = # connect model
    # once you successfully deleted a school,
    # go to back to the list page
    success_url = reverse_lazy('basic_app:list')
```
```html
<a href="{% url 'basic_app:detail' pk=school.pk %}">Cancel</a>
```

