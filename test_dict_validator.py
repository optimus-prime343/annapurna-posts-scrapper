from dict_validator import dict_validator


def test_dict_validator() -> None:
    user_dict = {"username": "Sachin123", "password": "Sachin123"}
    validation_rules = {
        "username": {
            "min": 5,
            "max": 10,
            "custom_validator": lambda x: x.startswith("S"),
        },
        "password": {"min": 5, "max": 10},
    }
    assert dict_validator(user_dict, validation_rules) is True
