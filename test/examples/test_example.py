import pytest

def test_equal_or_not_equal():
    assert 3 == 3
    assert 3 != 1


def test_is_instance():
    assert isinstance('string', str)
    assert not isinstance('10', int)


def test_boolean():
    validated = True
    assert validated is True
    assert ('hello' == 'world') is False


def test_type():
    assert type('Hello' is str)
    assert type('World' is not int)


class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years


@pytest.fixture
def default_student():
    return Student(first_name="John", last_name="Doe", major="Comp Sci", years=3)

def test_person_initialization(default_student: Student):
    assert default_student.first_name == "John", "First name should be John"
    assert default_student.last_name == "Doe"
    assert default_student.major == "Comp Sci"
    assert default_student.years == 3