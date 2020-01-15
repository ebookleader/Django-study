# 1. 사용자 모델 정의


## 장고 auth 프레임워크
- 가입, 로그인, 로그아웃 기능 제공


#### 사용자 인증
- 사용자 정보를 db에 저장하고, 저장된 데이터를 구분할 수 있는 유일한 키를 지정해서 사용자를 식별<br>
&rarr; 가입시 사용자를 구분할 수 있는 키를 사용자로부터 얻어오고 중복되지 않도록 함

- 비밀번호는 암호화 혹은 해시함수를 통해 저장 **(대부분 해싱함수를 통해 비밀번호 저장)**<br>
(ex. md5, sha1, sha256 등)


#### 커스텀 사용자 모델

- models.Model &rarr; class AbstractBaseUser &rarr; class AbstractUser &rarr; class User

- AbstractBaseUser

```python
class AbstractBaseUser(models.Model):
    # id는 자동생성
    password =
    last_login =
 
    def get_username(self):
    def clean(self):
    def save(self, *args, **kwargs):
    def natural_key(self):
 
    @property
    def is_anonoymous(self):
    @property
    def is_authenticated(self):
 
    def set_password(self, raw_password):
    def check_password(self, raw_password):
    def set_unusable_password(self):
    def has_usable_password(self):
    def get_full_name(self):
    def get_short_name(self):
 
    def get_session_auth_hash(self):
```

- AbstractUser

```python
class AbstractUser(AbstractBaseUser, PermissionMixin):
  # id, password, last_login 자동추가
  username =
  first_name =
  last_name =
  email =
  is_staff =
  is_active =
  date_joined =
 
  def clean(self):
  def get_full_name(self):
  def get_short_name(self):
  def email_user(self, subject, message, from_email=None, **kwargs):
```

- Abstract User 모델에 불필요한 필드나 변경하고 싶은 필드가 있는 경우 새로운 사용자 모델 정의

- step 1. 새로운 User 모델 정의

```python
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, UserManager)
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email', unique=True)
    name = models.CharField('name', max_length=30)
    is_staff = models.BooleanField('is_staff', default=False)
    is_active = models.BooleanField('is_active', default=True)
    date_joined = models.DateTimeField('date_joined', default=timezone.now)

    object = UserManager()

    # 이메일이 식별자
    USERNAME_FIELD = 'email'
    # 필수 입력값
    REQUIRED_FIELDS = ['name']

    class Meta:
        # 사용자가 읽기 쉬운 모델 객체의 이름, 관리자 화면에서 표시됨
        verbose_name = ('user')
        # 위와 동일하나 복수형으로 사용
        verbose_name_plural = _('users')
        swappable = 'AUTH_USER_MODEL'
```

```python
# setting.py
# 현재 사용자 모델이 무엇인지 설정 가능
AUTH_USER_MODEL = 'mySite.User'
```

- step 2. migrae & superuser 생성<br><br>
:exclamation: create_superuser() missing 1 required positional argument: 'username'<br><br>
:+1: 새로운 사용자 모델의 슈퍼유저 생성 메서드에 username이 필수로 설정되어 있어 발생한 오류로 매니저 코드에서 username 파라미터 삭제
```python
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
```

- step 3. admin 사이트에 새로운 사용자모델 추가
```python
from django.contrib import admin
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # 사이트에 보일 항목
    list_display = ('id','email','name','joined_at','last_login_at','is_superuser','is_active')
    # 클릭시 정보 수정으로 넘어가는 필드들
    list_display_links = ('id','email')
    # 상세정보에서 패스워드는 제외
    exclude = ('password',)

    def joined_at(self, obj):
        return obj.date_joined.strftime("%Y-%m-%d")
    def last_login_at(self, obj):
        if not obj.last_login:
            return ''
        return obj.last_login.strftime("%Y-%m-%d %H:%M")

    # 가장 최근에 가입한 사람부터 리스팅
    joined_at.admin_order_field = '-date_joined'  
    # 필드명
    joined_at.short_description = 'joined ddate'
    last_login_at.admin_order_field = 'last_login_at'
    # 필드명
    last_login_at.short_description = 'last login'
```

