# Django Level Four
## Index
1. Relative URLs with Templates
2. URL Template Inheritance
3. Template Filter and Custom Filter
---

1.Relative URLs with Templates
---------
Replace a hardcoded URL path in an href with a URL Template
```html
<a href="basicapp/index">Index</a>

can be changed to

<a href="{% url 'index' '%}">Index</a> 

when name='index' is in the urls.py file
```
```
Inside the urls.py file(app), add the variable app_name
and set this variable equal to app name

<a href="{% url 'basic_app:other' %}">the other page</a>

- left hand side: app_name
- right hand side: name with looks for
```

#### Example
+ urls.py (app)
```python
app_name = 'basic_app'

urlpatterns=[
    path('other/', views.other, name='other'),
]
```
+ urls.py (project)
```python
urlpatterns = [
    path('',views.index, name='index'),
    path('admin/', admin.site.urls),
    path('basic_app/',include('basic_app.urls')),
]
```
+ .html
```html
<a href="{% url 'basic_app:other' %}">the other page</a>
<a href="{% url 'admin:index'%}">link to admin</a>
<a href="{% url 'index' %}">linkt to index</a>

https:// ... /basic_app/other
```
