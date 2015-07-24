"""Setup content on the test ICAT server.

This test goes the complete cycle of setting up content on a test
server, including wiping all previous content, initializing the
server, creating a few example investigations, and adding some data to
these investigations.  It then compares the result with a reference
dump file.
"""

import os.path
import filecmp
import pytest
import icat
import icat.config
from conftest import require_icat_version
from conftest import gettestdata, callscript, filter_yaml_dump

# wipeicat uses JPQL search syntax.
require_icat_version("4.3.0")

testinput = gettestdata("example_data.yaml")
refdump = gettestdata("icatdump.yaml")
users = [ "acord", "ahau", "jbotu", "jdoe", "nbour", "rbeck" ]
refsummary = { "root": gettestdata("summary") }
for u in users:
    refsummary[u] = gettestdata("summary.%s" % u)


def test_init(wipeicat, icatconfigfile):
    args = ["-c", icatconfigfile, "-s", "root", testinput]
    callscript("init-icat.py", args)


@pytest.mark.parametrize("invname", [
    "08100122-EF", 
    "10100601-ST", 
    "12100409-ST"
])
def test_create_investigation(icatconfigfile, invname):
    args = ["-c", icatconfigfile, "-s", "useroffice", testinput, invname]
    callscript("create-investigation.py", args)

@pytest.mark.parametrize(("user", "sample"), [
    ("jbotu", "durol"), 
    ("ahau",  "nimnga"), 
    ("nbour", "nio")
])
def test_create_sampletype(icatconfigfile, user, sample):
    args = ["-c", icatconfigfile, "-s", user, testinput, sample]
    callscript("create-sampletype.py", args)

@pytest.mark.parametrize(("user", "invname"), [
    ("nbour", "08100122-EF"), 
    ("ahau",  "10100601-ST"), 
    ("nbour", "12100409-ST")
])
def test_addinvdata(icatconfigfile, user, invname):
    args = ["-c", icatconfigfile, "-s", user, testinput, invname]
    callscript("add-investigation-data.py", args)


def test_check_content(icatconfigfile, tmpdirsec):
    """Dump the resulting content and compare with a reference dump.
    """
    dump = os.path.join(tmpdirsec.dir, "dump.yaml")
    fdump = os.path.join(tmpdirsec.dir, "dump-filter.yaml")
    reffdump = os.path.join(tmpdirsec.dir, "dump-filter-ref.yaml")
    filter_yaml_dump(refdump, reffdump)
    args = ["-c", icatconfigfile, "-s", "root", "-f", "YAML", "-o", dump]
    callscript("icatdump.py", args)
    filter_yaml_dump(dump, fdump)
    assert filecmp.cmp(reffdump, fdump), "content of ICAT was not as expected"

def test_check_summary_root(icatconfigfile, tmpdirsec):
    """Check the number of objects for each class at the ICAT server.
    """
    summary = os.path.join(tmpdirsec.dir, "summary")
    ref = refsummary["root"]
    args = ["-c", icatconfigfile, "-s", "root"]
    with open(summary, "wt") as out:
        callscript("icatsummary.py", args, stdout=out)
    assert filecmp.cmp(ref, summary), "ICAT content was not as expected"

@pytest.mark.parametrize(("user"), users)
def test_check_summary_user(icatconfigfile, tmpdirsec, user):
    """Check the number of objects from a user's point of view.

    This checks which objects a given user may see and thus whether
    the (read) access rules work as expected.
    """
    summary = os.path.join(tmpdirsec.dir, "summary.%s" % user)
    ref = refsummary[user]
    args = ["-c", icatconfigfile, "-s", user]
    with open(summary, "wt") as out:
        callscript("icatsummary.py", args, stdout=out)
    assert filecmp.cmp(ref, summary), "ICAT content was not as expected"