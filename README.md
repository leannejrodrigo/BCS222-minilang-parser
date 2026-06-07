# MiniLang Parser

A BNF grammar specification and Python-based parser for a simple custom programming language, built as part of BCS 222 – Programming Paradigms.

---

## Overview

MiniLang is a minimal programming language designed to explore formal syntax definition and parsing. This project defines the language's grammar using **Backus-Naur Form (BNF)** and implements a **lexer and parser in Python** that validates code snippets against that grammar.

---

## Features

- Full BNF grammar specification for a simple programming language
- Support for:
  - Variable declarations (`int a;`, `float pi;`)
  - Assignment statements (`a = 5;`, `pi = 3.14;`)
  - Basic arithmetic operations (`+`, `-`, `*`, `/`)
  - Print statements (`print(a);`)
  - Conditional control flow (`if`/`else` statements)
- Python parser that validates code snippets and provides meaningful error messages
- 5 valid syntax examples and 3 invalid syntax examples with expected output

---

## BNF Grammar (Summary)

```
<Digit>         ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
<Integer>       ::= <Digit> | <Integer> <Digit>
<Float>         ::= <Integer> . <Integer>
<identifier>    ::= <IdentifierStart> | <identifier> <IdentifierEnd>
<Variable>      ::= <Type> <identifier> = <Value>
<expr>          ::= <Term> | <expr> <Math_OPS> <Term>
<Print>         ::= "print" "(" <expr> ")"
<IfStatement>   ::= "if" <Condition> ":" <NewLine> <space> <StatementList>
<ElseStatement> ::= "else" ":" <NewLine> <space> <StatementList>
```

See [`grammar/bnf_grammar.md`](grammar/bnf_grammar.md) for the full specification.

---

## Project Structure

```
minilang-parser/
├── grammar/
│   └── bnf_grammar.md       # Full BNF grammar definition
├── src/
│   └── parser.py            # Lexer and parser implementation
├── snippets/
│   ├── valid/               # Valid code snippet examples
│   └── invalid/             # Invalid code snippet examples (error cases)
├── tests/
│   └── test_parser.py       # Unit tests for the parser
├── report/
│   └── report.pdf           # Project report (grammar design & findings)
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- `rply` library

### Installation

```bash
git clone https://github.com/leannejrodrigo/minilang-parser.git
cd minilang-parser
pip install -r requirements.txt
```

### Running the Parser

```bash
python src/parser.py
```

The parser will run against all predefined snippets in the `snippets/` directory and print whether each one is **valid** or **invalid**, with error details where applicable.

---

## Example Output

```
[VALID]   int a = 5;               ✓ Parsed successfully
[VALID]   float pi = 3.14;         ✓ Parsed successfully
[VALID]   if (a > 0) { print(a); } ✓ Parsed successfully
[INVALID] int 9x = 3;              ✗ SyntaxError: identifier cannot start with a digit
[INVALID] print(;)                 ✗ SyntaxError: unexpected token ';'
```

---

## Dependencies

| Library | Purpose |
|--------|---------|
| `rply`  | Lexer and parser generation |

Install all dependencies with:

```bash
pip install -r requirements.txt
```

---

## Team Members

| Student ID | Name |
|------------|------|
| 20230003798 | Yasmin Akram Issa |
| 20210001983 | Leanne Jessica Rodrigo |
| 20230003378 | Fasmin Nizar |
| 20230003626 | Sidra Sheikh |

---

## Course Information

| Field | Detail |
|-------|--------|
| Course | BCS 222 – Programming Paradigms |
| Project | Part 1 – Designing a BNF Grammar |
| Instructor | Dr. Haythem El-Messiry |

---

## License

This project is submitted for academic purposes. All rights reserved.
