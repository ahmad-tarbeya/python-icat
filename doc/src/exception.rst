:mod:`icat.exception` --- Exception handling
============================================

.. py:module:: icat.exception

Helper
------

.. autofunction:: icat.exception.stripCause

Exceptions thrown by the ICAT or IDS server
-------------------------------------------

.. autoexception:: icat.exception.ServerError
    :members:
    :show-inheritance:

.. autoexception:: icat.exception.ICATError
    :members:
    :show-inheritance:

.. autoexception:: icat.exception.ICATParameterError
    :members:
    :show-inheritance:

.. autoexception:: icat.exception.ICATInternalError
    :members:
    :show-inheritance:

.. autoexception:: icat.exception.ICATPrivilegesError
    :members:
    :show-inheritance:

.. autoexception:: icat.exception.ICATNoObjectError
    :members:
    :show-inheritance:

.. autoexception:: icat.exception.ICATObjectExistsError
    :members:
    :show-inheritance:

.. autoexception:: icat.exception.ICATSessionError
    :members:
    :show-inheritance:

.. autoexception:: icat.exception.ICATValidationError
    :members:
    :show-inheritance:

.. autoexception:: icat.exception.ICATNotImplementedError
    :members:
    :show-inheritance:

.. autoexception:: icat.exception.IDSError
    :members:
    :show-inheritance:

.. autoexception:: icat.exception.IDSBadRequestError
    :members:
    :show-inheritance:

.. autoexception:: icat.exception.IDSDataNotOnlineError
    :members:
    :show-inheritance:

.. autoexception:: icat.exception.IDSInsufficientPrivilegesError
    :members:
    :show-inheritance:

.. autoexception:: icat.exception.IDSInsufficientStorageError
    :members:
    :show-inheritance:

.. autoexception:: icat.exception.IDSInternalError
    :members:
    :show-inheritance:

.. autoexception:: icat.exception.IDSNotFoundError
    :members:
    :show-inheritance:

.. autoexception:: icat.exception.IDSNotImplementedError
    :members:
    :show-inheritance:

.. autofunction:: icat.exception.translateError

Exceptions thrown by python-icat
--------------------------------

.. autoexception:: icat.exception.InternalError
    :members:
    :show-inheritance:

.. autoexception:: icat.exception.ConfigError
    :members:
    :show-inheritance:

.. autoexception:: icat.exception.QueryNullableOrderWarning
    :members:
    :show-inheritance:

.. autoexception:: icat.exception.ClientVersionWarning
    :members:
    :show-inheritance:

.. autoexception:: icat.exception.ICATDeprecationWarning
    :members:
    :show-inheritance:

.. autoexception:: icat.exception.VersionMethodError
    :members:
    :show-inheritance:

.. autoexception:: icat.exception.SearchResultError
    :members:
    :show-inheritance:

.. autoexception:: icat.exception.SearchAssertionError
    :members:
    :show-inheritance:

.. autoexception:: icat.exception.DataConsistencyError
    :members:
    :show-inheritance:

.. autoexception:: icat.exception.IDSResponseError
    :members:
    :show-inheritance:

.. autoexception:: icat.exception.GenealogyError
    :members:
    :show-inheritance:

Exception hierarchy
-------------------

The class hierarchy for the exceptions is::

  Exception
   +-- ServerError
   |    +-- ICATError
   |    |    +-- ICATParameterError
   |    |    +-- ICATInternalError
   |    |    +-- ICATPrivilegesError
   |    |    +-- ICATNoObjectError
   |    |    +-- ICATObjectExistsError
   |    |    +-- ICATSessionError
   |    |    +-- ICATValidationError
   |    |    +-- ICATNotImplementedError
   |    +-- IDSError
   |    |    +-- IDSBadRequestError
   |    |    +-- IDSDataNotOnlineError
   |    |    +-- IDSInsufficientPrivilegesError
   |    |    +-- IDSInsufficientStorageError
   |    |    +-- IDSInternalError
   |    |    +-- IDSNotFoundError
   |    |    +-- IDSNotImplementedError
   +-- InternalError
   +-- ConfigError
   +-- VersionMethodError
   +-- SearchResultError
   |    +-- SearchAssertionError
   +-- DataConsistencyError
   +-- IDSResponseError
   +-- GenealogyError
   +-- Warning
        +-- QueryNullableOrderWarning
        +-- ClientVersionWarning
        +-- DeprecationWarning
             +-- ICATDeprecationWarning

Here, ``Exception``, ``Warning``, and ``DeprecationWarning`` are
build-in exceptions from the Python standard library.
