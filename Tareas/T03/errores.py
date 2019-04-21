from typing import Callable, Any, Union, get_type_hints, List


def error_int_float_str(idx, el, d, parametros, args):
    def muestra(): pass
    if d[parametros[idx]] == Union[int, float]:
        if type(el) != type(1) and type(el) != type(1.2):
            raise Exception("Error de tipo: El elemento '{}',no es tipo '{}', es un '{}'".format(
                str(el), "float o int", type(el).__name__))
    elif d[parametros[idx]] == Callable[..., Any]:
        if type(el) != (type(muestra) or type((lambda x: x))):
            raise Exception("Error de tipo: El elemento '{}',no es tipo '{}', es un '{}'".format(
                str(el), "function or lambda", type(el).__name__))
    elif d[parametros[idx]] == List[float]:
        if type(el) != type([]):
            raise Exception("Error de tipo: El elemento '{}',no es tipo '{}', es un '{}'".format(
                str(el), "list", type(el).__name__))
    else:
        raise Exception("Error de tipo: El elemento '{}',no es tipo '{}', es un '{}'".format(
            str(el), d[parametros[idx]].__name__, type(el).__name__))


def error_union(idx, el, d, parametros, args):
    if type(el) != type(1) and type(el) != type(1.2):
        raise Exception("Error de tipo: El elemento '{}',no es tipo '{}', es un '{}'".format(
            str(el), "float o int", type(el).__name__))


def error_lista(idx, el, d, parametros, args):
    if type(el) != type([]):
        raise Exception("Error de tipo: El elemento '{}',no es tipo '{}', es un '{}'".format(
            str(el), "list", type(el).__name__))


def error_callable(idx, el, d, parametros, args):
    if type(el) != (type(_f) or type((lambda x: x))):
        raise Exception("Error de tipo: El elemento '{}',no es tipo '{}', es un '{}'".format(
            str(el), "function or lambda", type(el).__name__))


def error_tipo(funcion):
    d = get_type_hints(funcion)
    parametros = list(filter(lambda x: x in d, funcion.__code__.co_varnames))

    def _f(*args):
        if Union[int, float] in d.values():
            if len(parametros) != len(args):  # Esto es en el caso de las funciones de densidad
                [error_union(idx, el, d, parametros, args)
                 for idx, el in enumerate(args[1:])]
            else:
                [error_union(idx, el, d, parametros, args) for idx, el in enumerate(
                    args) if d[parametros[idx]] == Union[int, float]]
        elif Callable[..., Any] in d.values():
            [error_union(idx, el, d, parametros, args) for idx, el in enumerate(
                args) if d[parametros[idx]] == Callable[..., Any]]
        elif List[float] in d.values():
            [error_lista(idx, el, d, parametros, args) for idx, el in enumerate(
                args) if d[parametros[idx]] == List[float]]

        if len(parametros) != len(args):  # Esto es en el caso de las funciones de densidad
            [error_int_float_str(idx, el, d, parametros, args)
             for idx, el in enumerate(args[1:])]
        else:
            [error_int_float_str(idx, el, d, parametros, args) for idx, el in enumerate(
                args) if type(el) != d[parametros[idx]]]
        return funcion(*args)
    return _f
