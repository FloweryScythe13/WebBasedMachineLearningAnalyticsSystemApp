"""
Definition of urls for WebBasedMachineLearningAnalyticsSystemApp.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

from multi_correlation.views import index
from django.conf.urls.static import static
from multi_correlation import urls as multi_correlation_urls

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', index),
    url('app_demo/', include('app_demo.urls')),
    url(r'^ml_dnnreg/', include('ml_dnnreg.urls')),
    url(r'^multi_correlation$', include(multi_correlation_urls)),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about$', app.views.about, name='about'),
    #url(r'^login/$',
    #    django.contrib.auth.views.login,
    #    {
    #        'template_name': 'app/login.html',
    #        'authentication_form': app.forms.BootstrapAuthenticationForm,
    #        'extra_context':
    #        {
    #            'title': 'Log in',
    #            'year': datetime.now().year,
    #        }
    #    },
    #    name='login'),
    #url(r'^logout$',
    #    django.contrib.auth.views.logout,
    #    {
    #        'next_page': '/',
    #    },
    #    name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
    
]
