django-vaultkeeper-adaptor
==========================

.. image:: https://img.shields.io/travis/praekeltfoundation/django-vaultkeeper-adaptor/master.svg?style=flat-square
    :target: https://travis-ci.org/praekeltfoundation/vaultkeeper

.. image:: https://img.shields.io/codecov/c/github/praekeltfoundation/django-vaultkeeper-adaptor/master.svg?style=flat-square
    :target: https://codecov.io/github/praekeltfoundation/vaultkeeper?branch=develop

A small library that allows Django applications to consume Vaultkeeper output as resource secrets.

``django-vaultkeeper-adaptor`` supports the ``SET_ROLE`` operation `necessary to revoke dynamically-generated PostgreSQL credentials<https://github.com/jdelic/django-postgresql-setrole>`_.

Installing the Package
~~~~~~~~~~~~~~~~~~~~~~

Install the package for development with the following command:

``pip install -e .[test]``

Prerequisites
~~~~~~~~~~~~~

Technically, you do not need to launch your application with ``vaultkeeper`` to use this library, as it is simply an input adaptor.
However, using your app with ``vaultkeeper`` is strongly recommended.

It is assumed that the rest of your Vault workflow is already configured and running.

How to Use
~~~~~~~~~~

Ensure that ``django-vaultkeeper-adaptor`` is installed in your production environment.

Ensure that your Django application knows where the file containing your secrets will be.
In your ``settings.py``, replace your existing way of populating `DATABASES` and `BROKER_URL` with the following code:


```
cfg = environ.get('CREDENTIAL_PATH','')

if cfg != '':
    vk_adaptor = vaultkeeper_adaptor.VKAdaptor(
        config_path=cfg,
        DATABASES=DATABASES,
        BROKER_URL=BROKER_URL,
    )
    vk_adaptor.process_all()
```

``django-vaultkeeper-adaptor`` will read the ``vaultkeeper``-generated file containing application credentials and populate the supplied settings variables with values from the file, if they exist.
