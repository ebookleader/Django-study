## Index
1. 로그인
2. 로그아웃
3. 사용자 인증여부 
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

2.로그아웃
--------------
**- auth의 로그아웃 사용**
```python
# views.py

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
```

3.사용자 인증여부 확인
-------------------
**- 로그인을 검사하여 접근을 통제**
1. 데커레이터 사용 (함수형 뷰에서 사용)
```python
@login_required
def example_view(request):
    ...
```
2. 믹스인을 이용 (클래스형 뷰에서 사용)
```python
from django.contrib.auth.mixins import LoginRequiredMixin

class example_view(LoginRequiredMixin, View):
    ...
```
