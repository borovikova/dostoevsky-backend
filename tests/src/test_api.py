import pytest
import requests
import json

from dostoevsky import config

def test_api(postgres_db, test_rows, restart_api):
    url = config.get_api_url()
    payload = {
        "columns": ["totalConvicted", "primaryLifeSentence"],
        "split": ["part", "year"],
        "filters": {"year": ["2010"], "part": ["105ч.1", "106"]},
    }
    r = requests.get(f"{url}/data", params=payload)

    expected = [
        {
            "name": "Убийство",
            "category": "Тяжкие",
            "part": "105ч.2",
            "year": "2009",
            "totalConvicted": 9000,
            "primaryLifeSentence": 0,
        },
        {
            "name": "Убийство",
            "category": "Тяжкие",
            "part": "105ч.1",
            "year": "2009",
            "totalConvicted": 10000,
            "primaryLifeSentence": 1,
        },
    ]
    got = r.json()
    assert r.status_code == 201
    assert got == expected
