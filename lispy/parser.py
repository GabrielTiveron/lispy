from lark import Lark, InlineTransformer
from pathlib import Path

from .runtime import Symbol


class LispTransformer(InlineTransformer):
    number = float
    name = str
    def binop(self, op, left, right): 
        op = str(op)
        return (op, left, right)

def parse(src: str):
    """
    Compila string de entrada e retorna a S-expression equivalente.
    """
    return parser.parse(src)


def _make_grammar():
    """
    Retorna uma gramática do Lark inicializada.
    """

    path = Path(__file__).parent / 'grammar.lark'
    with open(path) as fd:
        grammar = Lark(fd, parser='lalr', transformer=LispTransformer())
    return grammar

parser = _make_grammar()
