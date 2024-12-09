from MathParser import *


a = "-1 + (((-5))) - 4 * 6 * (4 - 3) / (2 - 5 * 4)"

# y = MathParser(a)
y = math_parser(a)

print(a)
print(y)
print()
print(y.func)
print(y.args)
print()
print(y.args[2].func)
print(y.args[2].args)
print()
print(eval(a))
print(y.calculate())

