import pytest

from dostoevsky import model

pytestmark = pytest.mark.usefixtures("mappers")


def test_parts_mapper_can_insert_rows(session):
    session.execute(
        "INSERT INTO parts (name, part, year, category,\"totalConvicted\", \"primaryLifeSentence\") VALUES ('Убийство', '105ч.1', '2009', 'Тяжкие', 10000, 0);"
    )
    expected = [
        model.Part(
            name="Убийство",
            part="105ч.1",
            year="2009",
            category="Тяжкие",
            totalConvicted=10000,
            primaryLifeSentence=0,
        )
    ]
    assert session.query(model.Part).all() == expected


def test_parts_mapper_can_select_rows(session):
    new_row = model.Part(
        name="Убийство",
        part="105ч.1",
        year="2009",
        category="Тяжкие",
        totalConvicted=10000,
        primaryLifeSentence=0,
    )
    session.add(new_row)
    session.commit()

    rows = list(
        session.execute(
            'SELECT name, part, year, category, "totalConvicted", "primaryLifeSentence" FROM "parts"'
        )
    )
    assert rows == [("Убийство", "105ч.1", "2009", "Тяжкие", 10000, 0)]
