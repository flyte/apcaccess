import re
from collections import OrderedDict

from apcaccess import status
from .fixtures import SAMPLE_STATUS


def test_split_returns_list_of_strings():
    """
    Should return a list of strings.
    """
    lines = status.split(SAMPLE_STATUS)
    assert isinstance(lines, list)
    assert all([isinstance(x, str) for x in lines])


def test_split_removes_eof():
    """
    Should remove the EOF string from the end of the status.
    """
    lines = status.split(SAMPLE_STATUS)
    assert SAMPLE_STATUS.endswith(status.EOF)
    last_element = next(reversed(lines))
    assert not last_element.endswith(status.EOF)


def test_split_removes_newlines():
    """
    Should remove the newline characters from the ends of each line.
    """
    lines = status.split(SAMPLE_STATUS)
    assert not any([x.endswith("\n") for x in lines])


def test_split_removes_null_and_length():
    """
    Should remove the null and length value at the beginning of each line.
    """
    lines = status.split(SAMPLE_STATUS)
    assert SAMPLE_STATUS.startswith("\x00\x18")
    assert not any((
        "\x00" in lines[0],
        "\x18" in lines[0]
    ))


def test_split_removes_blank_lines():
    """
    Should not return any blank lines.
    """
    lines = status.split(SAMPLE_STATUS)
    assert all(len(x) > 0 for x in lines)


def test_parse_returns_ordereddict():
    """
    Should return an OrderedDict.
    """
    parsed = status.parse(SAMPLE_STATUS)
    assert isinstance(parsed, OrderedDict)


def test_parse_splits_each_line_on_sep():
    """
    Should split each line on the separator character.
    """
    lines = SAMPLE_STATUS.split("\x00")
    parsed = status.parse(SAMPLE_STATUS)
    assert all([status.SEP in x for x in lines if x])
    assert not any([status.SEP in x for x in zip(parsed.items())])


def test_parse_doesnt_split_values_containing_sep():
    """
    Shouldn't split a value up if it contains the separator character.
    """
    lines = status.split(SAMPLE_STATUS)
    # Check that there is a line on which there are more than one SEPs
    assert any([x.count(status.SEP) > 1 for x in lines])
    parsed = status.parse(SAMPLE_STATUS)
    assert all([len(x) == 2 for x in parsed.items()])
    assert any([status.SEP in x for x in parsed.values()])


def test_parse_removes_extraneous_whitespace():
    """
    Should remove leading and trailing whitespace from keys and values.
    """
    lines = status.split(SAMPLE_STATUS)
    # Check that there are some lines which have whitespace next to SEP
    reg = re.compile(r".*?(?:\s+{0}|{0}\s+).*?".format(re.escape(status.SEP)))
    assert any([reg.match(x) for x in lines])
    parsed = status.parse(SAMPLE_STATUS)
    for key, value in parsed.items():
        assert key.strip() == key
        assert value.strip() == value

def test_parse_strips_units():
    """
    Should strip units from the values if requested.
    """
    parsed = status.parse(SAMPLE_STATUS, strip_units=True)
    for value in parsed.values():
        for unit in status.ALL_UNITS:
            assert not value.endswith(unit)

def test_parse_doesnt_strip_units():
    """
    Should not strip units from the values if not requested.
    """
    parsed = status.parse(SAMPLE_STATUS)
    has_units = False
    for value in parsed.values():
        for unit in status.ALL_UNITS:
            if value.endswith(unit):
                has_units = True
    assert has_units


def test_strip_units_removes_units():
    """
    Should remove all units from the ends of the lines.
    """
    lines = ["100 %s" % x for x in status.ALL_UNITS]
    lines.append("100")
    stripped = status.strip_units_from_lines(lines)
    assert all([x == "100" for x in stripped])


def test_print_status_runs():
    """
    Should print status.
    """
    status.print_status(SAMPLE_STATUS)


def test_print_status_runs_with_strip_units():
    """
    Should print status without units.
    """
    status.print_status(SAMPLE_STATUS, strip_units=True)
