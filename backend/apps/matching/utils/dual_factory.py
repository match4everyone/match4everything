from match4everyone.configuration.A import A
from match4everyone.configuration.B import B


def instanciate_for_participants(func, args_a=None, args_b=None):
    """
    Create A and B instance for generator function.

    Whenever we create a class that needs to have access to the participant p_type,
    but never is passed such a thing, we use this.

    There are probably way more elegant things... looking forward to suggestions.
    """
    args_a = args_a if args_a is not None else {}
    args_b = args_b if args_b is not None else {}

    a_class = func(A.url_name, **args_a)
    b_class = func(B.url_name, **args_b)
    return {"A": a_class, A.url_name: a_class, "B": b_class, B.url_name: b_class}
