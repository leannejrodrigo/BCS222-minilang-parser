from rply import LexerGenerator, ParserGenerator
from rply.token import BaseBox

# ──────────────────────────────────────────
# Lexer
# ──────────────────────────────────────────

lg = LexerGenerator()

lg.add('FLOAT',   r'\d+\.\d+')
lg.add('NUMBER',  r'\d+')
lg.add('PRINT',   r'print')
lg.add('IF',      r'if')
lg.add('ELSE',    r'else')
lg.add('TRUE',    r'True')
lg.add('FALSE',   r'False')
lg.add('INT',     r'int')
lg.add('FLOATTYPE', r'float')
lg.add('STRING',  r'\"[^\"]*\"')
lg.add('ID',      r'[a-zA-Z_][a-zA-Z0-9_]*')
lg.add('ASSIGN',  r'=')
lg.add('PLUS',    r'\+')
lg.add('MINUS',   r'-')
lg.add('MUL',     r'\*')
lg.add('DIV',     r'/')
lg.add('GT',      r'>')
lg.add('LT',      r'<')
lg.add('GTE',     r'>=')
lg.add('LTE',     r'<=')
lg.add('NEQ',     r'!=')
lg.add('LPAREN',  r'\(')
lg.add('RPAREN',  r'\)')
lg.add('LBRACE',  r'\{')
lg.add('RBRACE',  r'\}')
lg.add('SEMI',    r';')
lg.add('COLON',   r':')
lg.ignore(r'\s+')

lexer = lg.build()


# ──────────────────────────────────────────
# AST Nodes
# ──────────────────────────────────────────

class Node(BaseBox):
    pass

class NumberNode(Node):
    def __init__(self, value):
        self.value = value

class FloatNode(Node):
    def __init__(self, value):
        self.value = value

class BinOpNode(Node):
    def __init__(self, left, op, right):
        self.left, self.op, self.right = left, op, right

class PrintNode(Node):
    def __init__(self, expr):
        self.expr = expr

class VarDeclNode(Node):
    def __init__(self, var_type, name, value):
        self.var_type, self.name, self.value = var_type, name, value

class IfNode(Node):
    def __init__(self, condition, body, else_body=None):
        self.condition, self.body, self.else_body = condition, body, else_body

class ConditionNode(Node):
    def __init__(self, left, op, right):
        self.left, self.op, self.right = left, op, right

class IdentifierNode(Node):
    def __init__(self, name):
        self.name = name


# ──────────────────────────────────────────
# Parser
# ──────────────────────────────────────────

pg = ParserGenerator(
    ['FLOAT', 'NUMBER', 'PRINT', 'IF', 'ELSE', 'TRUE', 'FALSE',
     'INT', 'FLOATTYPE', 'STRING', 'ID', 'ASSIGN', 'PLUS', 'MINUS',
     'MUL', 'DIV', 'GT', 'LT', 'GTE', 'LTE', 'NEQ',
     'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMI', 'COLON'],
    precedence=[
        ('left', ['PLUS', 'MINUS']),
        ('left', ['MUL', 'DIV']),
    ]
)

@pg.production('program : statement_list')
def program(p):
    return p[0]

@pg.production('statement_list : statement')
def statement_list_single(p):
    return [p[0]]

@pg.production('statement_list : statement_list statement')
def statement_list_multi(p):
    return p[0] + [p[1]]

@pg.production('statement : var_decl')
@pg.production('statement : print_stmt')
@pg.production('statement : if_stmt')
def statement(p):
    return p[0]

@pg.production('var_decl : INT ID ASSIGN expr SEMI')
def var_decl_int(p):
    return VarDeclNode('int', p[1].getstr(), p[3])

@pg.production('var_decl : FLOATTYPE ID ASSIGN expr SEMI')
def var_decl_float(p):
    return VarDeclNode('float', p[1].getstr(), p[3])

@pg.production('print_stmt : PRINT LPAREN expr RPAREN SEMI')
def print_stmt(p):
    return PrintNode(p[2])

@pg.production('if_stmt : IF LPAREN condition RPAREN LBRACE statement_list RBRACE')
def if_stmt(p):
    return IfNode(p[2], p[5])

@pg.production('if_stmt : IF LPAREN condition RPAREN LBRACE statement_list RBRACE ELSE LBRACE statement_list RBRACE')
def if_else_stmt(p):
    return IfNode(p[2], p[5], p[9])

@pg.production('condition : expr GT expr')
def cond_gt(p):
    return ConditionNode(p[0], '>', p[2])

@pg.production('condition : expr LT expr')
def cond_lt(p):
    return ConditionNode(p[0], '<', p[2])

@pg.production('condition : expr GTE expr')
def cond_gte(p):
    return ConditionNode(p[0], '>=', p[2])

@pg.production('condition : expr LTE expr')
def cond_lte(p):
    return ConditionNode(p[0], '<=', p[2])

@pg.production('condition : expr NEQ expr')
def cond_neq(p):
    return ConditionNode(p[0], '!=', p[2])

@pg.production('condition : expr ASSIGN ASSIGN expr')
def cond_eq(p):
    return ConditionNode(p[0], '==', p[3])

@pg.production('expr : expr PLUS expr')
def expr_add(p):
    return BinOpNode(p[0], '+', p[2])

@pg.production('expr : expr MINUS expr')
def expr_sub(p):
    return BinOpNode(p[0], '-', p[2])

@pg.production('expr : expr MUL expr')
def expr_mul(p):
    return BinOpNode(p[0], '*', p[2])

@pg.production('expr : expr DIV expr')
def expr_div(p):
    return BinOpNode(p[0], '/', p[2])

@pg.production('expr : LPAREN expr RPAREN')
def expr_paren(p):
    return p[1]

@pg.production('expr : NUMBER')
def expr_number(p):
    return NumberNode(int(p[0].getstr()))

@pg.production('expr : FLOAT')
def expr_float(p):
    return FloatNode(float(p[0].getstr()))

@pg.production('expr : ID')
def expr_id(p):
    return IdentifierNode(p[0].getstr())

@pg.error
def error_handler(token):
    raise ValueError(f"Syntax error at '{token.getstr()}' (type: {token.gettokentype()})")

parser = pg.build()


# ──────────────────────────────────────────
# Parse helper
# ──────────────────────────────────────────

def parse(code):
    try:
        tokens = lexer.lex(code)
        parser.parse(tokens)
        return True, "Parsed successfully"
    except Exception as e:
        return False, str(e)


# ──────────────────────────────────────────
# Test snippets
# ──────────────────────────────────────────

valid_snippets = [
    ("int a = 5;",                                    "Variable declaration (int)"),
    ("float pi = 3.14;",                              "Variable declaration (float)"),
    ("int result = (3 + 4) * 2;",                     "Arithmetic with parentheses"),
    ("print(10 + 5);",                                "Print with arithmetic"),
    ("if (a > 0) { print(a); }",                      "If statement"),
]

invalid_snippets = [
    ("int = 5;",          "Missing identifier"),
    ("print(;)",          "Missing expression in print"),
    ("if a > 0 { }",      "Missing parentheses in condition"),
]

if __name__ == "__main__":
    print("=" * 55)
    print("  VALID SNIPPETS")
    print("=" * 55)
    for code, label in valid_snippets:
        ok, msg = parse(code)
        status = "✓ VALID  " if ok else "✗ INVALID"
        print(f"[{status}] {label}")
        print(f"           Code : {code}")
        print(f"           Info : {msg}")
        print()

    print("=" * 55)
    print("  INVALID SNIPPETS")
    print("=" * 55)
    for code, label in invalid_snippets:
        ok, msg = parse(code)
        status = "✓ VALID  " if ok else "✗ INVALID"
        print(f"[{status}] {label}")
        print(f"           Code : {code}")
        print(f"           Info : {msg}")
        print()
