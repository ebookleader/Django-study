# Django Level Five
## Index
1. Passwords
2. User Models
3. Registration
4. Logins
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

3.Registration
---------

4.Logins
---------

