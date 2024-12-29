from hyperon import *
metta = MeTTa()
expr1 = metta.parse_single('(+ 1 2)')
print(expr1, type(expr1))
print(metta.evaluate_atom(expr1))
expr2 = E(OperationAtom('+', lambda a, b: a + b),
          ValueAtom(1), ValueAtom(2))
print(metta.evaluate_atom(expr2))


print(type(expr2))