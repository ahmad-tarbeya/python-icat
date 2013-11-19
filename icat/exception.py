"""Exception handling.
"""

import suds

__all__ = [
    # Exceptions thrown by the ICAT server
    'ICATError', 'ICATParameterError', 'ICATInternalError', 
    'ICATPrivilegesError', 'ICATNoObjectError', 'ICATObjectExistsError', 
    'ICATSessionError', 'ICATValidationError', 
    'translateError', 
    # icat.client
    'ClientVersionWarning', 'VersionMethodError', 
    # icat.config
    'ConfigError', 
    # icat.icatcheck
    'GenealogyError',
    ]


# ========== Exceptions thrown by the ICAT server ==========

class ICATError(Exception):
    """Base class for the errors raised by the ICAT server.
    """
    def __init__(self, webfault):
        super(ICATError, self).__init__(str(webfault))
        self.fault = webfault.fault
        self.document = webfault.document
        self.message = webfault.fault.detail.IcatException.message
        self.offset = webfault.fault.detail.IcatException.offset
        self.type = webfault.fault.detail.IcatException.type

class ICATParameterError(ICATError):
    """Generally indicates a problem with the arguments made to a
    call.
    """
    pass

class ICATInternalError(ICATError):
    """May be caused by network problems, database problems, GlassFish
    problems or bugs in ICAT.
    """
    pass

class ICATPrivilegesError(ICATError):
    """Indicates that the authorization rules have not matched your
    request.
    """
    pass

class ICATNoObjectError(ICATError):
    """Is thrown when something is not found.
    """
    pass

class ICATObjectExistsError(ICATError):
    """Is thrown when trying to create something but there is already
    one with the same values of the constraint fields.
    """
    pass

class ICATSessionError(ICATError):
    """Is used when the sessionId you have passed into a call is not
    valid or if you are unable to authenticate.
    """
    pass

class ICATValidationError(ICATError):
    """Marks an exception which was thrown instead of placing the
    database in an invalid state.
    """
    pass

IcatExceptionTypeMap = {
    "BAD_PARAMETER": ICATParameterError,
    "INTERNAL": ICATInternalError,
    "INSUFFICIENT_PRIVILEGES": ICATPrivilegesError,
    "NO_SUCH_OBJECT_FOUND": ICATNoObjectError,
    "OBJECT_ALREADY_EXISTS": ICATObjectExistsError,
    "SESSION": ICATSessionError,
    "VALIDATION": ICATValidationError,
}
"""Map exception types thrown by the ICAT server to Python classes."""

def translateError(error):
    """Translate a suds.WebFault into the corresponding ICATError."""
    if isinstance(error, suds.WebFault):
        Class = IcatExceptionTypeMap[error.fault.detail.IcatException.type]
        return Class(error)
    else:
        raise TypeError("Invalid argument type '%s'." % type(error))


# ========== Exceptions raised in icat.client ==========

class ClientVersionWarning(Warning):
    """Warn that the version of the ICAT server is not supported by
    the client.
    """
    def __init__(self, version=None, comment=None):
        if version is None:
            icatstr = "this ICAT version"
        else:
            icatstr = "ICAT version %s" % version
        if comment is None:
            msg = ("%s is not supported, "
                   "expect problems and weird behavior!" % icatstr)
        else:
            msg = ("%s is not supported (%s), "
                   "expect problems and weird behavior!" % (icatstr, comment))
        super(ClientVersionWarning, self).__init__(msg)

class VersionMethodError(Exception):
    """Call of an ICAT API method that is not supported in the version
    of the ICAT server.
    """
    def __init__(self, method, version=None):
        if version is None:
            icatstr = "this ICAT version"
        else:
            icatstr = "ICAT version %s" % version
        msg = ("%s is not supported in %s." % (method, icatstr))
        super(VersionMethodError, self).__init__(msg)


# ========== Exceptions raised in icat.config ==========

class ConfigError(Exception):
    """Error getting configuration options."""
    pass


# ========== Exceptions raised in icat.icatcheck ==========

class GenealogyError(Exception):
    """Error in the genealogy of entity types."""
    pass