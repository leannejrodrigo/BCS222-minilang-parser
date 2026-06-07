# MiniLang BNF Grammar Specification

## Primitives

```
<Digit>             ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9

<Alphabet>          ::= A | B | C | D | E | F | G | H | I | J | K | L | M
                      | N | O | P | Q | R | S | T | U | V | W | X | Y | Z
                      | a | b | c | d | e | f | g | h | i | j | k | l | m
                      | n | o | p | q | r | s | t | u | v | w | x | y | z

<Math_OPS>          ::= - | + | / | * | = | ^ | √ | %

<Boolean>           ::= True | False

<Space>             ::= " "

<Comp_OPS>          ::= > | < | <= | >= | = | != | || | &&

<Special_Characters>::= ! | @ | # | $ | % | ^ | & | * | ( | ) | _ | { | }
                      | \ | | | [ | ] | : | ; | ' | " | ? | / | > | < | .
                      | , | - | + | = | √ | π

<Empty_Space>       ::= "\n" | "\t" | "  "

<NewLine>           ::= \n
```

## Numbers

```
<Integer>           ::= <Digit> | <Integer> <Digit>

<Float>             ::= <Integer> . <Integer>
```

## Strings & Characters

```
<SubCharacter>      ::= <Digit> | <Special_Characters> | <Alphabet>

<Character>         ::= <Alphabet> | <Character> <SubCharacter>

<SubString>         ::= <Character> | <Float> | <SubString> <Character> | <Float>

<String>            ::= <SubString> | <Space>
```

## Types & Values

```
<Type>              ::= <Float> | <Integer> | <String>

<Value>             ::= <Integer> | <Float> | <String>
```

## Identifiers

```
<IdentifierStart>   ::= <Alphabet> | _

<IdentifierEnd>     ::= <Digit> | _ | <Alphabet>

<identifier>        ::= <IdentifierStart> | <identifier> <IdentifierEnd>
```

## Variables

```
<Variable>          ::= <Type> <identifier> = <Value>
```

## Expressions

```
<expr>              ::= <Term> | <expr> <Math_OPS> <Term>

<Term>              ::= <Factor> | <Term> * <Factor> | <Term> / <Factor>

<Factor>            ::= <Integer> | <Float> | "(" <expr> ")"
```

## Statements

```
<Print>             ::= "print" "(" <expr> ")"

<IfStatement>       ::= "if" <Condition> ":" <NewLine> <Space> <StatementList> <NewLine> <ElseStatement>

<ElseStatement>     ::= "else" ":" <NewLine> <Space> <StatementList>
```
