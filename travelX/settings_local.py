DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        # 'NAME': 'travelx',
        'NAME': 'travelx',
        'USER' : 'travelx',
        'PASSWORD' : 'shubh1987',
        'HOST' : 'travelx.cuotggeqscvh.ap-southeast-2.rds.amazonaws.com',
        'PORT' : '5432',
    }
}

LIST_FOR_MAILS=['shubhamdrolia87@gmail.com']

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'shubhamdrolia87@gmail.com'
EMAIL_HOST_PASSWORD = 'saurabh1990'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'shubhamdrolia87@gmail.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'