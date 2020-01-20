## Index
1. 가입시 이메일 보내기
2. 인증 페이지 생성
3. 재발송
---


1.가입시 이메일 보내기
---------


**- 설정파일에서 gmail 설정**
```python
# settings.py

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'awesome@gmail.com'
EMAIL_HOST_PASSWORD = '7h1515myp455w0rd'
EMAIL_USE_TLS = True

# gmail 설정에서 보안수준 낮은 앱 허용 설정
```


**- is_active**
- auth 프레임워크의 모델 백엔드는 is_active가 True인 사용자만 정상적인 사용자로 인증함<br>
&rarr; 이메일 인증 전까지 is_active를 False로 저장
```python
# models.py

    is_active = models.BooleanField('is_active', default=False)

    ###

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

```

**- form_valid**
```python
# views.py

from django.contrib import messages
# 사용자 데이터를 가지고 해시 데이터를 만들어주는 객체
from django.contrib.auth.tokens import default_token_generator
from userRegistration import settings

class UserRegistrationView(CreateView):
    model = get_user_model()
    form_class = UserRegistrationForm
    success_url = reverse_lazy('mySite:index')
    
    verify_url = '/mySite/verify'
    token_generator = default_token_generator

    # 오버라이드
    # 폼객체의 필드값들이 유효성 검증을 통과할경우 호출되어 각 필드값들 db에 저장
    # 유효한 폼 데이터로 처리할 로직을 코딩
    # 반드시 super()함수 호출
    def form_valid(self, form):
        response = super().form_valid(form)
        #저장된 데이터는 폼객체의 instance변수에 저장됨
        if form.instance:
            self.send_verification_email(form.instance)
        return response

    def send_verification_email(self, user):
        # 생성된 사용자 고유의 토큰을 생성
        token = self.token_generator.make_token(user)
        # (subject, message, from_email=None, **kwargs)
        user.email_user('Congratulations!',
                        'Please verify your email.{}'.format(self.build_verification_link(user,token)),
                        from_email = settings.EMAIL_HOST_USER)

    # 
    def build_verification_link(self, user, token):
        # ex) http://127.0.0.1:8000/mySite/12/verify/token(5d9-bb...)
        # UserVerificationView로 넘어감
        return '{}/mySite/{}/verify/{}/'.format(self.request.META.get('HTTP_ORIGIN'), user.pk, token)

```


2.인증페이지 생성
---------


**- 인증뷰 생성**
```python
# views.py

from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView

class UserVerificationView(TemplateView):
    model = get_user_model()
    redirect_url = '/mySite/login'
    token_generator = default_token_generator

    def get(self, request, *args, **kwargs):
        if self.is_valid_token(**kwargs):
            messages.info(request, 'success')
        else:
            messages.error(request, 'failed')
        # 인증 성공여부 상관없이 로그인 페이지로 이동
        return HttpResponseRedirect(self.redirect_url)

    def is_valid_token(self, **kwargs):
        pk = kwargs.get('pk')
        token = kwargs.get('token')
        user = self.model.object.get(pk=pk)
        # 사용자 pk와 token을 가지고 해당 사용자의 정상적인 token값인지 확인
        is_valid = self.token_generator.check_token(user, token)
        # 인증이 실패할 경우는 is_active를 False로 바꾸는 대신 무시하고 실패 메시지만 출력
        if is_valid:
            user.is_active = True
            user.save()
        return is_valid
```
```python
# urls.py

path('mySite/<pk>/verify/<token>/', UserVerificationView.as_view()),
```

**- 인증 메일 스타일 수정**
- 이메일은 css가 적용되지 않는 경우가 많으므로 태그안에 속성으로 디자인
- ex) grapejs같은 에디터 사용

**- 뷰에서 템플릿 렌더링**
```python
# views.py

class UserRegistrationView(CreateView):
    ###
    email_template_name = 'mySite/registration_verification.html'
    ###

    def send_verification_email(self, user):
        token = self.token_generator.make_token(user)
        url = self.build_verification_link(user, token)
        subject = 'Congratulations!'
        message = 'Please verify your email.{}'.format(url)
        # render함수는 HttpResponse객체를 반환
        # content에 렌더링된 메시지가 저장되어있는데 byte로 인코딩 되어있으므로 utf-8로 디코딩 해줘야함
        html_message = render(self.request, self.email_template_name, {'url':url}).content.decode('utf-8')
        user.email_user(subject, message, settings.EMAIL_HOST_USER, html_message = html_message)
        messages.info(self.request, 'we send a email. please verify your email')
```

3.재발송
---------


**- 재발송 뷰 생성**
- 중복되는 메소드와 클래스변수 mixin에 선언
```python
# mixins.py

from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render
from userRegistration import settings

class VerifyEmailMixin:
    email_template_name = 'mySite/registration_verification.html'
    token_generator = default_token_generator

    def send_verification_email(self, user):
        token = self.token_generator.make_token(user)
        url = self.build_verification_link(user, token)
        subject = 'Congratulations!'
        message = 'Please verify your email.{}'.format(url) 
        html_message = render(self.request, self.email_template_name,{'url':url}).content.decode('utf-8')
        user.email_user(subject, message, settings.EMAIL_HOST_USER, html_message = html_message)
        messages.info(self.request, 'we send a email. please verify your email')

    def build_verification_link(self, user, token):
        return '{}/mySite/{}/verify/{}/'.format(self.request.META.get('HTTP_ORIGIN'), user.pk, token)

```

```python
# views.py

from .mixins import VerifyEmailMixin

class UserRegistrationView(VerifyEmailMixin, CreateView):
    model = get_user_model()
    form_class = UserRegistrationForm
    success_url = reverse_lazy('mySite:index')
    verify_url = '/mySite/verify'

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.instance:
            self.send_verification_email(form.instance)
        return response
        
class ResendVerifyEmailView(VerifyEmailMixin, FormView):
    model = get_user_model()
    form_class = VerificationEmailForm
    success_url = 'login'
    # 해당 페이지로 자동 렌더링
    template_name = 'mySite/resend_verify_email.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = self.model.object.get(email=email)
        except self.model.DoesNotExist:
            messages.error(self.request, '알 수 없는 사용자 입니다.')
        else:
            self.send_verification_email(user)
        return super().form_valid(form)
```
```python
# forms.py

# 폼의 필드는 유효성 검증을 할 때 정의된 default_validators 리스트의 각 원소들을 
# 입력된 값을 전달하여 함수처럼 호출
class VerificationEmailForm(forms.Form):
        email = EmailField(widget=forms.EmailInput(attrs={'autofocus': True}), validators=(EmailField.default_validators + [RegisteredEmailValidator()]))
```
```python
# validators.py

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

class RegisteredEmailValidator:
    user_model = get_user_model()
    code = 'invalid'

    # 필드의 유효성 검증 필터는 __call__메소드를 오버라이드 해줘야함
    def __call__(self, email):
        try:
            user = self.user_model.objects.get(email=email)
        except self.user_model.DoesNotExist:
            raise ValidationError('가입되지 않은 이메일입니다.', code=self.code)
        else:
            if user.is_active:
                raise ValidationError('이미 인증되어 있습니다.', code=self.code)

        return
```
**- 페이지 생성후 링크 연결**






