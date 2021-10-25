import model
from repository import SqlAlchemyRepository


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
            'SELECT name, part, year, category, totalConvicted FROM "parts"'
        )
    )
    assert rows == [("Убийство", "105ч.1", "2011", "Тяжкие", 5000)]


def test_repository_get_all(session):
    session.execute(
        "INSERT INTO parts (name, part, year, category, totalConvicted, primaryLifeSentence) VALUES "
        '("Убийство", "105ч.1", "2009", "Тяжкие", 10000, 1), ("Убийство", "105ч.2", "2009", "Тяжкие", 9000, 0)'
    )
    expected = [
        model.Part(
            name="Убийство",
            part="105ч.1",
            year="2009",
            category="Тяжкие",
            totalConvicted=10000,
            primaryLifeSentence=1,
        ),
        model.Part(
            name="Убийство",
            part="105ч.2",
            year="2009",
            category="Тяжкие",
            totalConvicted=9000,
            primaryLifeSentence=0,
        ),
    ]
    repo = SqlAlchemyRepository(session)
    got = repo.get_all()
    assert got == expected


def test_repository_can_filter_data(session):
    session.execute(
        "INSERT INTO parts (name, part, year, totalConvicted, primaryLifeSentence) VALUES "
        '("Убийство", "105ч.1", "2010",  10056, 3),'
        '("Убийство с отягчающими", "105ч.2", "2010",  6001, 0),'
        '("Убийство матерью", "106", "2010",  5368, 1),'
        '("Убийство", "105ч.1", "2011",  4579, 0),'
        '("Убийство с отягчающими", "105ч.2", "2011",  8932, 4),'
        '("Убийство матерью", "106", "2011",  10689, 1)'
    )
    filters = {
        "year": ["2010"],
        "part": ["105ч.1", "106"],
        "param": ["totalConvicted", "primaryLifeSentence"],
    }

    repo = SqlAlchemyRepository(session)
    got = repo.get_filtered(filters)
    expected = [
        model.Part(
            name="Убийство",
            part="105ч.1",
            year="2010",
            category="",
            totalConvicted=10056,
            primaryLifeSentence=3,
        ),
        model.Part(
            name="Убийство матерью",
            part="106",
            year="2010",
            category="",
            totalConvicted=5368,
            primaryLifeSentence=1,
        ),
    ]
    assert got == expected


def test_repository_can_get_parameters_with_aggregation_by_year(session):
    assert False


def test_repository_can_get_parameters_with_aggregation_by_parameter(session):
    assert False


def test_repository_can_get_parameters_with_aggregation_by_year_and_parameter(session):
    assert False
