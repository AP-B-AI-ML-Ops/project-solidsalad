from exercise.load import collect


def test_generate_query_params():
    actual = collect.generate_query_params("test", 1, 10)

    expected = {
        "$$app_token": "test",
        "$where": "tpep_pickup_datetime between '2021-01-01T00:00:00' and '2021-02-01T00:00:00'",
        "$limit": 10,
    }

    assert actual == expected
