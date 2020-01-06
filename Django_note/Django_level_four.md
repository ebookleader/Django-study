# Django Level Four
## Index
1. Relative URLs with Templates
2. URL Template Inheritance
3. Template Filters and Custom Filters
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

2.URL Template Inheritance
---------
Set same html code to the base.html file and inherit it using template inheritance
1. find the repetitive parts of project
2. create a base template of them
3. set the tags in the base template
4. extend and call those tags anywhere

Example
+ base.html
```html
<bunch of html like navbars>
<body>
  {% block block_name %}
  {% endblock %}
</body>
</More footer html>
```
+ other.html
```html
<!DOCTYPE html>
{% extends "basic_app/base.html" %}
    {% block block_name %}  
    <HTML specific for other.html>
    <HTML specific for other.html>
    {% endblock %}
```

3.Template filters and custom filters
---------
Django provides a ton of easy to implement template filters that allow you to effect the injection before displaying it to the user

1) Template filter
```html
{{ value|filter:"parameter" }}

Example 

{{ text|upper }}

{{ number|add:"99"}}
```

2) Custom filter
- create a new folder (ex. templatetags)
- make \_\_init__.py file, this file tells python to treat this as a module
- make custom file (ex. my_extras.py), this is the file actually put custom templates
```python
from django import template

register = template.Library()

#decorators
@register.filter(name='cut')
def cut(value, arg):
    return value.replace(arg,'')
```
```html
{{ text|cut:'hello' }}
```
#### Reference
<https://docs.djangoproject.com/en/1.10/topics/templates/#filters>


