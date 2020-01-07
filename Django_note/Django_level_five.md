# Django Level Five
## Index
1. Passwords
2. User Models
3. Registration
4. Login/Logout
---

1.Passwords
---------
1. use some built-in apps and they are under the INSTALLED_APPS in settings.py
* **'django.contrib.auth'** and **'django.contrib.contenttypes'**
* after add them, you have to migrate
 
 2. store passwords safely
 * **Never store passwords as plain text**
 ```python
 pip install bcrypt
 pip install django[argon2]
 ```
 * settings.py
 ```python
 PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS':{'min_length':9}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
 ```
 

2.User Models
---------
- User object has a Username, Email, Password, First Name, Last Name
- models.py
```python
class anotherClass(models.Model):

 # create relationship
 user = models.OneToOneField(User, on_delete=models.CASCADE)
 
 # add additional attribute
 
 ## image and url attribute
 # pip install pillow to use Image
 
 site = models.URLField(blank=True)
 pic = models.ImageField(upload_to='..', blank=True)
 
 def __str__(self):
  return self.user.username
```
- forms.py
```python
from django import forms
from django.contrib.auth.models import User
from .models import UserProfileInfo

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password')
        
class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site','profile_pic')
```

3.Registration
---------
- views.py
```python
def register(request):
 registered=False
 
 if request.method == 'POST':
 
  # get info from forms
  user_form = UserForm(data=request.POST)
  ...
  
  #check forms are valid
  if user_form.is_valid():
  
   #save to database
   user = user_form.save()
   
   #hash the password
   user.set_password(user.password)
   
   #update
   user.save()
   
   ## dealing pictures 
   
   # we can manipulate the data before saving it to database by setiing commit=False
   profile = profile_form.save(commit=False)
   
   # set relationship
   profile.user = user
  
   # check if they provided a profile picture
   # save
   
   registered = True
   
 return render(request, 'basic_app/registration.html',
    {'user_form':user_form, 'profile_form':profile_form, 'registered':registered})
```
- registration.html
```html
{% if registered %}
{% else %}
# form
{% endif %}
```

4.Login/Logout
---------
1. Login
- adding the login url in settings
```python
LOGIN_URL = '/.. ../user_login'
```
- views.py
```python
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
```
```python
def user_login(request):

 # get the username and password supplied by login.html
 username = request.POST.get('username')
 ...
 
 # use built-in authentication function to check whether user is in database
 user = authenticate(username= .. , password= ..)
 
 if user:
 
  # check the account is active
  if user.is_activate:
  
   # login
   login(request, user)
   
   return HttpResponseRedirect(reverse('..')
```
- create login.html
- editing the urls.py

2. Logout
- using built-in decorators for access
```python
@login_required
def user_logout(request):
 logout(request)
 return HttpResponseRedirect(reverse('..')
```
- base.html
```html
{% if user.is_authenticated %}
# logout
{% else %}
# login
{% endif %}
```
- editing the urls.py
