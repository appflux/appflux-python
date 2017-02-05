Appflux Python
----

[Appflux](http://www.appflux.io) integration for python for seemless exception tracking.

Key Featuers
----
* Reports unhandles exceptions via email & also provides a simple but intutive UI for exception traking.
* Allows custom notifications.
* Gives you hooks for before & after the exception.

Installation
----

1) Via PyPy

```
pip install appflux-python
```

2) Via GitHub, just clone the repo and run:

```
python setup.py install
```

Setup
----
You will need to create an account at [Appflux](http://www.appflux.io) and get an AppID.

In settings.py

* Put ```appflux``` in your INSTALLED_APPS
* put ```appflux.django.AppfluxMiddleware``` in your MIDDLEWARE_CLASSES
* ```APPFLUX_APP_KEY = 'xxxxxxxxxx'```
* Restart your app and you are all set to track exceptions.

Hooks
----

This Package gives you two the ability to add before and after hooks for an exception. You just need to pass the method/hook in before_notify/after_notify.

```
appflux_exception = AppfluxException()
appflux_exception.before_notify(method_name)
```

In this before/after hook you will recieve two arguments self & request.

Add Tabs
----

To add a tab in your request you can use ```before_notify``` hook, like this

```
  def method_name(self, request):
  self.add_tab('test', 'testing exception')
```
