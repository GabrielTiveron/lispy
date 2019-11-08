from lark import Lark, InlineTransformer
from pathlib import Path

from .runtime import Symbol

class LispTransformer(InlineTransformer):

    number = float
    name   = str

    def binop(self, op, left, right):
        op = Symbol(op)
        return list(tuple((op, left, right)))

    def binop_alt(self, left, op, right):
        op = Symbol(op)
        return list(tuple((op, left, right)))

    def binop_alt2(self, left, op, right):
        op = [op]
        return list(tuple((op, left, right)))

    def let_alt(self, *args):
        *defines, ops = args
        return list(tuple((Symbol.LET, defines, ops)))

    def lambda_alt(self, *args):
        name, *params, op = args
        return list(tuple((Symbol.DEFINE, Symbol(name), list(tuple((Symbol.LAMBDA, params, op))))))

    def lambda_alt2(self, *args):
        *params, ops = args;
        return list(tuple((Symbol.LAMBDA, params, ops)))

    def assign(self, value, expr):
        return list(tuple((value, expr)))

    def bool(self, term):
        return term == '#t'

    def string(self, string):
        string = string.replace('\\n', '\n')
        string = string.replace('\\t', '\t')
        string = string.replace('\\"', '\"')
        return string[1:-1]

    def list(self, *args):
        return list(args)

    def condition(self, test, then, other):
        return list(tuple((Symbol.IF, test, then, other)))

    def condition_alt(self, test, then, alt):
        return list(tuple((Symbol.IF, test, then, alt)))

    def else_alt(self, arg):
        return arg

    def condition_alt2(self, *args):
        x, y, k = args
        return list(tuple((Symbol.IF, x, y, k)))

    def quote(self, quote):
        return list(tuple((Symbol.QUOTE, quote)))

    def symbol(self, symbol):
        return Symbol(symbol)

    def let(self, defines, ops):
        return list(tuple((Symbol.LET, defines, ops)))

    def lambdas(self, args, func):
        return list(tuple((Symbol.LAMBDA, args, func)))

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
