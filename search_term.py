from typing import Optional


has_function_ran_already: bool = False
search_term: Optional[str] = None


def print_char(word: str) -> None:
    global has_function_ran_already
    global search_term
    if has_function_ran_already and search_term == word:
        return
    for char in word:
        print(char)
    has_function_ran_already = True
    search_term = word


def main() -> None:
    print_char("Sachin")
    print_char("Sachin")
    print_char("Sachin")
    print_char("Sachin")
    print_char("DESPACITO")
    print_char("DESPACITO")
    print_char("DESPACITO")


if __name__ == "__main__":
    main()
