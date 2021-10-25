import model


def test_parameters_mapper_can_insert_rows(session):
    session.execute(
        "INSERT INTO parameters (name, part, parameter, value, year, category) VALUES "
        '("Убийство", "105ч.1", "totalConvicted", 10719, "2009", "Тяжкие"),'
        '("Убийство", "105ч.1", "totalConvicted", 10000, "2010", "")'
    )
    expected = [
        model.Parameter(
            "Убийство", "105ч.1", "totalConvicted", 10719, "2009", "Тяжкие"
        ),
        model.Parameter("Убийство", "105ч.1", "totalConvicted", 10000, "2010"),
    ]
    assert session.query(model.Parameter).all() == expected


def test_parameters_mapper_can_select_rows(session):
    new_row = model.Parameter(
        "Убийство", "105ч.1", "totalConvicted", 5000, "2011", "Тяжкие"
    )
    session.add(new_row)
    session.commit()

    rows = list(
        session.execute(
            'SELECT name, part, parameter, value, year, category FROM "parameters"'
        )
    )
    assert rows == [("Убийство", "105ч.1", "totalConvicted", 5000, "2011", "Тяжкие")]
