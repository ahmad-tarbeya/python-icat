"""Test adding a validation hook for entity objects.
"""

import pytest
import icat
import icat.config
from conftest import getConfig


@pytest.fixture(scope="module")
def client(setupicat):
    conf = getConfig(confSection="nbour")
    client = icat.Client(conf.url, **conf.client_kwargs)
    client.login(conf.auth, conf.credentials)
    return client

@pytest.fixture(scope="module")
def dataset(client, request):
    """Create a temporary Dataset for the tests.
    """
    inv = client.assertedSearch("Investigation [name='08100122-EF']")[0]
    dstype = client.assertedSearch("DatasetType [name='raw']")[0]
    dataset = client.new("dataset",
                         name="test_07_entity_validate", complete=False,
                         investigation=inv, type=dstype)
    dataset.create()
    def cleanup():
        client.delete(dataset)
    request.addfinalizer(cleanup)
    return dataset


def validate_param(self):
    """Validate parameter objects.

    Check that NUMERIC parameters have numericValue set and do not
    have stringValue or dateTimeValue set.
    """
    if self.type.valueType == "NUMERIC":
        if self.stringValue is not None:
            raise ValueError("NUMERIC parameter cannot set stringValue")
        if self.dateTimeValue is not None:
            raise ValueError("NUMERIC parameter cannot set dateTimeValue")
        if self.numericValue is None:
            raise ValueError("NUMERIC parameter must set numericValue")
    elif self.type.valueType == "STRING":
        if self.dateTimeValue is not None:
            raise ValueError("STRING parameter cannot set dateTimeValue")
        if self.numericValue is not None:
            raise ValueError("STRING parameter cannot set numericValue")
        if self.stringValue is None:
            raise ValueError("STRING parameter must set stringValue")
    elif self.type.valueType == "DATE_AND_TIME":
        if self.numericValue is not None:
            raise ValueError("DATE_AND_TIME parameter cannot set numericValue")
        if self.stringValue is not None:
            raise ValueError("DATE_AND_TIME parameter cannot set stringValue")
        if self.dateTimeValue is None:
            raise ValueError("DATE_AND_TIME parameter must set dateTimeValue")
    else:
        raise ValueError("Invalid valueType '%s'" % self.type.valueType)


def test_invalid_string_value(client, dataset):
    """Try setting stringValue on a NUMERIC parameter.
    """
    client.typemap['parameter'].validate = validate_param
    ptype = client.assertedSearch("ParameterType [name='Magnetic field']")[0]
    assert ptype.valueType == "NUMERIC"
    param = client.new("datasetParameter", dataset=dataset, type=ptype)
    param.numericValue = 7
    param.stringValue = "seven"
    with pytest.raises(ValueError) as err:
        param.create()
    assert 'NUMERIC parameter cannot set stringValue' in str(err.value)
    assert param.id is None

def test_invalid_missing_numeric_value(client, dataset):
    """Try creating a NUMERIC parameter without setting any value.
    """
    client.typemap['parameter'].validate = validate_param
    ptype = client.assertedSearch("ParameterType [name='Magnetic field']")[0]
    assert ptype.valueType == "NUMERIC"
    param = client.new("datasetParameter", dataset=dataset, type=ptype)
    with pytest.raises(ValueError) as err:
        param.create()
    assert 'NUMERIC parameter must set numericValue' in str(err.value)
    assert param.id is None

def test_valid_numeric_value(client, dataset):
    """Create a valid NUMERIC parameter.
    """
    client.typemap['parameter'].validate = validate_param
    ptype = client.assertedSearch("ParameterType [name='Magnetic field']")[0]
    assert ptype.valueType == "NUMERIC"
    param = client.new("datasetParameter", dataset=dataset, type=ptype)
    param.numericValue = 7
    param.create()
    assert param.id is not None