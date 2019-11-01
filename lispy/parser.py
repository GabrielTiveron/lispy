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
    return read_from_tokens(src.replace('(', ' ( ').replace(')', ' ) ').split())

def read_from_tokens(tokens: list):

    if len(tokens) == 0:
        raise SyntaxError('Empty tokens')
    token = tokens.pop(0)
    if token == '(':
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif token == ')':
        raise SyntaxError('unexpected )')
    else:
        try: 
            return int(token)
        except ValueError:
            try: 
                return float(token)
            except ValueError:
                return Symbol(token)

def _make_grammar():
    """
    Retorna uma gramática do Lark inicializada.
    """

    path = Path(__file__).parent / 'grammar.lark'
    with open(path) as fd:
        grammar = Lark(fd, parser='lalr', transformer=LispTransformer())
    return grammar

parser = _make_grammar()
