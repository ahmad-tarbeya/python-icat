"""pytest configuration.
"""

from __future__ import print_function
import sys
import os
import os.path
import re
import shutil
import tempfile
import logging
import pytest
import icat


# Note that pytest captures stderr, so we won't see any logging by
# default.  But since Suds uses logging, it's better to still have
# a well defined basic logging configuration in place.
logging.basicConfig(level=logging.INFO)

testdir = os.path.dirname(__file__)


# ============================= helper ===============================

class tmpSessionId:
    """Temporarily switch to another sessionId in an ICAT client.
    """
    def __init__(self, client, sessionId):
        self.client = client
        self.saveSessionId = client.sessionId
        self.sessionId = sessionId
    def __enter__(self):
        self.client.sessionId = self.sessionId
        return self.client
    def __exit__(self, type, value, tb):
        self.client.sessionId = self.saveSessionId


def gettestdata(fname):
    fname = os.path.join(testdir, "data", fname)
    assert os.path.isfile(fname)
    return fname


def callscript(scriptname, args):
    script = os.path.join(testdir, "scripts", scriptname)
    cmd = [sys.executable, script] + args
    print("\n>", *cmd)
    ret = os.spawnv(os.P_WAIT, sys.executable, cmd)
    assert ret == 0


def filter_yaml_dump(infile, outfile):
    """Strip the header information from a YAML dump file.

    We need this because we want to compare the content of dump
    files.  But the header information is supposed to change
    independently of the content.
    """
    substre = re.compile(r"^# (Date|Service|ICAT-API|Generator): .*$")
    with open(infile, 'rt') as inf, open(outfile, 'wt') as outf:
        while True:
            l = inf.readline()
            if not l:
                break
            l = re.sub(substre, r"# \1: ###", l)
            outf.write(l)


def filter_xml_dump(infile, outfile):
    """Strip the header information from a XML dump file.

    We need this because we want to compare the content of dump
    files.  But the header information is supposed to change
    independently of the content.
    """
    substre = re.compile(r"^\s*<(date|service|apiversion|generator)>.*</\1>$")
    with open(infile, 'rt') as inf, open(outfile, 'wt') as outf:
        while True:
            l = inf.readline()
            if not l:
                break
            l = re.sub(substre, r"  <\1>###</\1>", l)
            outf.write(l)


# ============================ fixtures ==============================

# Deliberately not using the 'tmpdir' fixture provided by pytest,
# because it seem to use a predictable directory name in /tmp wich is
# insecure.

class TmpDir(object):
    """Provide a temporary directory.
    """
    def __init__(self):
        self.dir = tempfile.mkdtemp(prefix="python-icat-test-")
    def __del__(self):
        self.cleanup()
    def cleanup(self):
        if self.dir:
            shutil.rmtree(self.dir)
        self.dir = None

@pytest.fixture(scope="session")
def tmpdirsec(request):
    tmpdir = TmpDir()
    request.addfinalizer(tmpdir.cleanup)
    return tmpdir


@pytest.fixture(scope="session")
def icatconfigfile():
    fname = os.path.join(testdir, "data", "icat.cfg")
    if not os.path.isfile(fname):
        pytest.skip("no test ICAT server configured")
    return fname


# ============================= hooks ================================

def pytest_report_header(config):
    """Add information on the icat package used in the tests.
    """
    modpath = os.path.dirname(os.path.abspath(icat.__file__))
    return [ "python-icat: %s (%s)" % (icat.__version__, icat.__revision__), 
             "             %s" % (modpath) ]
