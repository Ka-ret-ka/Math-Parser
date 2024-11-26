from abc import ABCMeta, abstractmethod
from typing import Any


class MathFunction(metaclass = ABCMeta):
    @abstractmethod
    def __init__(self, data: Any):
        self.args: list[Any]
        self.func: type
    @abstractmethod
    def __repr__(self) -> str:
        pass
    @abstractmethod
    def calculate(self) -> (int | float):
        pass



class Integer(MathFunction):
    def __init__(self, data: int):
        self.args: list[int] = [data]
        self.func = type(self)

    def __repr__(self):
        return str(self.args[0])

    def calculate(self) -> int:
        return self.args[0]



class Float(MathFunction):
    def __init__(self, data: float):
        self.args: list[float] = [data]
        self.func = type(self)

    def __repr__(self):
        return str(self.args[0])

    def calculate(self) -> float:
        return self.args[0]



class Add(MathFunction):
    def __init__(self, data: list[MathFunction]):
        self.args: list[MathFunction] = data
        self.func = type(self)

    def __repr__(self):
        ret_str: str = ''
        for i in self.args:
            if (type(i) == InvOfMul):
                ret_str += '1' + str(i)
            ret_str += str(i) + ' + '
        return ret_str[:-3].replace('+ -', '- ')

    def calculate(self) -> (int | float):
        ret = 0
        for i in self.args:
            ret += i.calculate()
        return ret



class Mul(MathFunction):
    def __init__(self, data: list[MathFunction]):
        self.args: list[MathFunction] = data
        self.func = type(self)

    def __repr__(self):
        ret_str: str = ''
        for i in range(0, len(self.args)):
            if (type(self.args[i]) not in [InvOfAdd, Add] or (type(self.args[i]) == InvOfAdd and i == 0)):
                ret_str += str(self.args[i])
            else:
                ret_str += '(' + str(self.args[i]) + ')'
            ret_str += ' * '
        return ret_str[:-3].replace('* /', '/')

    def calculate(self) -> (int | float):
        ret = 1
        for i in self.args:
            ret *= i.calculate()
        return ret



class InvOfAdd(MathFunction):
    def __init__(self, data: MathFunction):
        self.args: list[MathFunction] = [data]
        self.func = type(self)

    def __repr__(self):
        if (type(self.args[0]) == Add):
            return '-(' + str(self.args[0]) + ')'
        if (type(self.args[0]) == InvOfMul):
            return '-' + str(self.args[0])
        if (type(self.args[0]) == InvOfAdd):
            return str(self.args[0].args[0])
        return '-' + str(self.args[0])

    def calculate(self) -> (int | float):
        return -self.args[0].calculate()



class InvOfMul(MathFunction):
    def __init__(self, data: MathFunction):
        self.args: list[MathFunction] = [data]
        self.func = type(self)

    def __repr__(self):
        if (type(self.args[0]) in [InvOfAdd, Mul, Add]):
            return '/ (' + str(self.args[0]) + ')'
        if (type(self.args[0]) == InvOfMul):
            return str(self.args[0])
        return '/ ' + str(self.args[0])

    def calculate(self) -> float:
        return 1 / self.args[0].calculate()



def __building_tree(expression: str) -> MathFunction:
    def __init_multiplier(expression: str) -> MathFunction:
        # Рекурсивно обрабатываем выражения в скобках
        if (expression[0] == '[' and expression[-1] == ']'):
            return __building_tree(pos_of_brackets[int(expression[1:-1])])
        if (expression[0] == '/'):
            return InvOfMul(__init_multiplier(expression[1:]))
        if (expression[0] == '-'):
            return InvOfAdd(__init_multiplier(expression[1:]))
        if ('.' in expression or ',' in expression):
            return Float(float(expression))
        return Integer(int(expression))

    # Поиск "внешних" скобок
    pos_of_brackets: dict[int, str] = dict()
    end: int
    point: int = 0
    # Справа налево
    for i in range(len(expression) - 1, -1, -1):
        if (expression[i] == ')'):
            if (point == 0):
                end = i
            point += 1
        if (expression[i] == '('):
            if (point == 1):
                pos_of_brackets[i] = expression[i + 1 : end]
                # Замена скобок на ключ словаря (позиция открывающей скобки, относительно начальной строки)
                expression = expression[:i] + f"[{i}]" + expression[end + 1:]
            point -= 1

    # Делим выражение на слагаемые
    expr_list: Any = expression.replace('-', '+-').removeprefix('+').split('+')
    for i in range(len(expr_list)):
        # Каждое слагаемое делим на множители
        expr_list[i] = expr_list[i].replace('/', '*/').split('*')
        # Каждый множитель в слагаемом инициализируем
        for j in range(len(expr_list[i])):
            expr_list[i][j] = __init_multiplier(expr_list[i][j])
        # Инициализируем слагаемое
        if (len(expr_list[i]) != 1):
            expr_list[i] = Mul(expr_list[i])
        else:
            expr_list[i] = expr_list[i][0]
    # Инициализируем сумму
    if (len(expr_list) != 1):
        expr_list = Add(expr_list)
    else:
        expr_list = expr_list[0]

    return expr_list



def math_parser(expression: str) -> MathFunction:
    return __building_tree(expression.replace(' ', ''))


