## Index
1. 로그인
2. 
---


1.로그인
---------


**- LoginView 상속을통한 구현**
```python
# views.py

from django.contrib.auth.views import LoginView

class UserLoginView(LoginView):
    # template_name 변수 정의
    template_name = 'mySite/login_form.html'
```


**- settings 파일에 LOGIN_REDIRECT_URL 변수 설정**
```python
# settings.py

LOGIN_REDIRECT_URL = 'mySite:index'
```


**- 로그인 여부에따른 메뉴**
```html
<!-- base.html -->

{% if request.user.is_authenticated %}

{% if not request.user.is_authenticated %}
```


**- text로 되어있는 email필드 input태그 변경**
<br>
폼클래스에서 CharField를 EmailField로 변경
```python
# forms.py

# AuthenticationForm 상속받아서 LoginForm 클래스 정의후
# username을 EmailField로, widget을 EmailInput으로 변경
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = EmailField()
```


**- LoginForm을 UserLoginView에서 설정**
<br>
authentication_form 변수에 LoginForm을 설정
```python
# views.py

class UserLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'mySite/login_form.html'
```
