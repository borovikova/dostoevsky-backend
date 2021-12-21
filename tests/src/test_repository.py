import pytest

from dostoevsky import model
from dostoevsky.repository import SqlAlchemyRepository

pytestmark = pytest.mark.usefixtures("mappers")


@pytest.fixture
def test_rows(session):
    session.execute(
        'INSERT INTO parts (name, part, year, "totalConvicted", "primaryLifeSentence") VALUES '
        "('Убийство', '105ч.1', '2010',  10056, 3),"
        "('Убийство с отягчающими', '105ч.2', '2010',  6001, 0),"
        "('Убийство матерью', '106', '2010',  5368, 1),"
        "('Убийство', '105ч.1', '2011',  4579, 0),"
        "('Убийство с отягчающими', '105ч.2', '2011',  8932, 4),"
        "('Убийство матерью', '106', '2011',  10689, 1)"
    )


def test_repository_can_save_a_parameter(session):
    row = [
        model.Part(
            name="Убийство",
            part="105ч.1",
            totalConvicted=5000,
            year="2011",
            category="Тяжкие",
        )
    ]

    repo = SqlAlchemyRepository(session)
    repo.add(row)
    session.commit()

    rows = list(
        session.execute(
            'SELECT name, part, year, category, "totalConvicted" FROM "parts"'
        )
    )
    assert rows == [("Убийство", "105ч.1", "2011", "Тяжкие", 5000)]


def test_repository_split_by_year_part(session):
    session.execute(
        "INSERT INTO parts (name, part, year, category, \"totalConvicted\", \"primaryLifeSentence\") VALUES ('Убийство', '105ч.1', '2009', 'Тяжкие', 10000, 1), ('Убийство', '105ч.2', '2009', 'Тяжкие', 9000, 0)"
    )
    expected = [
        ("Убийство", "Тяжкие", "105ч.2", "2009", 9000, 0),
        ("Убийство", "Тяжкие", "105ч.1", "2009", 10000, 1),
    ]
    repo = SqlAlchemyRepository(session)
    columns = ["totalConvicted", "primaryLifeSentence"]
    got = repo.get_data(columns, split=["part", "year"])
    assert got == expected


def test_repository_can_filter_data(session, test_rows):
    filters = {"year": ["2010"], "part": ["105ч.1", "106"]}
    columns = ["totalConvicted", "primaryLifeSentence"]

    repo = SqlAlchemyRepository(session)
    got = repo.get_data(columns, filters, split=["part", "year"])
    expected = [
        ("Убийство", "", "105ч.1", "2010", 10056, 3),
        ("Убийство матерью", "", "106", "2010", 5368, 1),
    ]
    assert got == expected


def test_repository__split_by_year(session, test_rows):
    repo = SqlAlchemyRepository(session)
    columns = ["totalConvicted", "primaryLifeSentence"]
    got = repo.get_data(columns, split=["year"])
    expected = [("2011", 4579 + 8932 + 10689, 5), ("2010", 10056 + 6001 + 5368, 4)]
    assert got == expected


def test_repository__split_by_part(session, test_rows):
    repo = SqlAlchemyRepository(session)
    columns = ["totalConvicted", "primaryLifeSentence"]
    got = repo.get_data(columns, split=["part"])
    expected = [
        ("Убийство матерью", "", "106", 5368 + 10689, 2),
        ("Убийство с отягчающими", "", "105ч.2", 6001 + 8932, 4),
        ("Убийство", "", "105ч.1", 10056 + 4579, 3),
    ]
    assert got == expected


def test_repository_no_split(session, test_rows):
    repo = SqlAlchemyRepository(session)
    columns = ["totalConvicted", "primaryLifeSentence"]
    got = repo.get_data(columns, split=[])
    expected = [(10056 + 6001 + 5368 + 4579 + 8932 + 10689, 3 + 0 + 1 + 0 + 4 + 1)]
    assert got == expected
