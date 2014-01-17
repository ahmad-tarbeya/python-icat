#! /usr/bin/python

import sys
from setuptools import setup
import icat
import re

DOCLINES         = icat.__doc__.split("\n")
DESCRIPTION      = DOCLINES[0]
LONG_DESCRIPTION = "\n".join(DOCLINES[2:])
VERSION          = icat.__version__
AUTHOR           = icat.__author__
URL              = "http://code.google.com/p/icatproject/wiki/PythonIcat"
m = re.match(r"^(.*?)\s*<(.*)>$", AUTHOR)
(AUTHOR_NAME, AUTHOR_EMAIL) = m.groups() if m else (AUTHOR, None)

extra_setup_params = {}
if sys.version_info >= (3, 0):
    extra_setup_params["use_2to3"] = True

setup(
    name = "python-icat",
    version = VERSION,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    author = AUTHOR_NAME,
    author_email = AUTHOR_EMAIL,
    url = URL,
    license = "BSD-2-Clause",
    requires = ["suds"],
    packages = ["icat"],
    # It may be that the package also works with other Python
    # versions.  In particular 3.0 and 3.1 should work, I guess.  But
    # these are the versions I have access to and I tested the package
    # with.  Python 3 requires the jurko fork of Suds.
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    **extra_setup_params
)

