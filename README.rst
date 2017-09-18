django-vaultkeeper-adaptor
==========================

.. image:: https://img.shields.io/travis/praekeltfoundation/django-vaultkeeper-adaptor/master.svg?style=flat-square
    :target: https://travis-ci.org/praekeltfoundation/vaultkeeper

.. image:: https://img.shields.io/codecov/c/github/praekeltfoundation/django-vaultkeeper-adaptor/master.svg?style=flat-square
    :target: https://codecov.io/github/praekeltfoundation/vaultkeeper?branch=develop

|
| A small library that allows Django applications to consume `vaultkeeper <https://github.com/praekeltfoundation/vaultkeeper>`_ output as resource secrets.
| 
| ``django-vaultkeeper-adaptor`` supports the ``SET_ROLE`` operation `necessary to revoke dynamically-generated PostgreSQL credentials <https://github.com/jdelic/django-postgresql-setrole>`_.

Installing the Package
----------------------

| Clone this project and install the package from source with the following commands in the root directory of the repository:

| ``$ pip install -e .``
| 
| Install the package for development with the following command:
| 
| ``$ pip install -e .[test]``

Prerequisites
-------------

| Technically, you do not need to launch your application with ``vaultkeeper`` to use this library, as it is simply an input adaptor. However, using your app with ``vaultkeeper`` is strongly recommended.
| 
| It is assumed that the rest of your Vault workflow is already configured and running. If you are using the PostgreSQL secret backend with Django, it is necessary to use ``django-postgresql-setrole`` in your application as well.

How to Use
----------

| Ensure that ``django-vaultkeeper-adaptor`` is installed in your production environment.
| 
| Ensure that your Django application knows where the file containing your secrets will be. In your ``settings.py``, replace your existing way of populating ``DATABASES`` and ``BROKER_URL`` with the following code:


.. code-block:: Python

    cfg = environ.get('CREDENTIAL_PATH','')
    
    if cfg != '':
        vk_adaptor = vaultkeeper_adaptor.VKAdaptor(
            config_path=cfg,
            DATABASES=DATABASES,
            BROKER_URL=BROKER_URL,
        )
        vk_adaptor.process_all()

|
| ``django-vaultkeeper-adaptor`` will read the ``vaultkeeper``-generated file containing application credentials and populate the supplied settings variables with values from the file, if they exist.
|
| Note that ``CREDENTIAL_PATH`` in the above example is an environment variable set with the output location of ``vaultkeeper`` secrets. You can supply your application with this value in a different manner if you wish.
