"""
Django settings for Dev04 project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')k1-@pye$u1%!7(0=u(wvsan8y@+cb+11f1@&aha)6t)nik*83'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'projects',
    'interfaces',
    #'projects.apps.ProjectsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Dev04.urls'

TEMPLATES = [
    {
        # a.指定模板引擎：指的是html是由哪个引擎进行解析
        # b.常用的模板引擎，DjangoTemplates、Jinja2
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # c.指定html页面或者html模板存放的路径，可以添加多个路径
        # d.是Django搜索html页面或者html模板的路径
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        # e.指定子应用下是否有html页面
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Dev04.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


#用数据库之前需要安装mysqlclient库，使Django能够正常和MYSQL通信，Django支持mysql5.7及以上版本
DATABASES = {
    # 在Django数据库的标识，如果有多个数据库就添加多个字典用,号分割
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        'ENGINE': 'django.db.backends.mysql',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'NAME': 'dev04',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': 3306,
    }
    # 'default': {
    #     # 'ENGINE': 'django.db.backends.sqlite3',
    #     'ENGINE': 'django.db.backends.mysql',
    #     # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #     'NAME': 'python_04',
    #     'USER': 'root',
    #     'PASSWORD': '123456',
    #     'HOST': 'localhost',
    #     'PORT': 3306,
    # }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

# LANGUAGE_CODE = 'en-us'
#
# TIME_ZONE = 'UTC'
# 指定简体中文
LANGUAGE_CODE = 'zh-hans'
# 指定时区
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

# 在全局配置文件settings.py文件中的REST_FRAMEWORK字典里修改DRF框架的配置
REST_FRAMEWORK = {
    'NON_FIELD_ERRORS_KEY': 'errors',
}