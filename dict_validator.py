from typing import Any, Callable, Dict, Optional, Union


def validate_length(
    value: Union[str, int],
    min_length: Optional[int],
    max_length: Optional[int],
) -> bool:
    if min_length is not None and max_length is not None:
        if isinstance(value, str):
            return min_length <= len(value) <= max_length
        else:
            return min_length <= value <= max_length
    elif min_length is not None:
        if isinstance(value, str):
            return len(value) >= min_length
        else:
            return value >= min_length
    elif max_length is not None:
        if isinstance(value, str):
            return len(value) <= max_length
        else:
            return value <= max_length
    else:
        return True


def dict_validator(
    dict: Dict[str, Any],
    validation_rules: Dict[str, Dict[str, Any]],
) -> bool:
    for key, value in dict.items():
        if isinstance(value, Dict):
            return dict_validator(value, validation_rules[key])
        validation_rule = validation_rules.get(key)
        if validation_rule is None:
            return True
        min_ = validation_rule.get("min")
        max_ = validation_rule.get("max")
        custom_validator: Optional[Callable[[Any], bool]] = validation_rule.get(
            "custom_validator"
        )
        if (
            min_ is not None
            and not isinstance(min_, int)
            or max_ is not None
            and not isinstance(max_, int)
        ):
            raise ValueError("min and max must be integers")
        if min_ is not None and max_ is not None and min_ >= max_:
            raise ValueError("min must be less than max")
        if custom_validator is not None:
            if not callable(custom_validator):
                raise ValueError("custom_validator must be callable")
            if not isinstance(custom_validator(value), bool):
                raise ValueError("custom_validator must return a boolean")
            return custom_validator(value)
        return validate_length(value, min_, max_)
    return True


def main() -> None:
    user_dict = {"username": "Sachin123", "password": "Sachin123"}
    user_dict_validation_rules = {
        "username": {"min": 6, "max": 20},
        "password": {"min": 6, "max": 100},
    }
    is_valid = dict_validator(user_dict, user_dict_validation_rules)
    print(is_valid)


if __name__ == "__main__":
    main()
