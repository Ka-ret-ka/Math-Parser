from abc import ABCMeta, abstractmethod



class MathFunction(metaclass=ABCMeta):
    @abstractmethod
    def __str__(self):
        pass



class Integer(MathFunction):
    def __init__(self, data: int):
        self.data = data

    def __str__(self):
        return str(self.data)



class Float(MathFunction):
    def __init__(self, data: float):
        self.data = data

    def __str__(self):
        return str(self.data)



# class Rational(MathFunction):
#     def __init__(self, numerator: int, denominator: int):
#         self.numerator = numerator
#         self.denominator = denominator


#     def print(self):
#         print(f'{self.numerator}/{self.denominator}', end='')



class Add(MathFunction):
    def __init__(self, data: list[MathFunction]):
        self.data = data

    def __str__(self):
        return str([str(i) for i in self.data])[2:-2].replace("', '", ' + ')



class Mul(MathFunction):
    def __init__(self, data: list[MathFunction]):
        self.data = data

    def __str__(self):
        return str([str(i) for i in self.data])[2:-2].replace("', '", '*')



class MathParser(MathFunction):
    def __init__(self, expr_str: str):
        self.__expr = MathParser.__building_tree(expr_str)

    def __str__(self):
        return str(self.__expr)

    def __building_tree(expr_str: str):
        expr_str = expr_str.replace(',', '.')
        # Делим выражение на слагаемые
        expr_list = expr_str.split('+')
        # Каждое слагаемое делим на множители
        for i in range(len(expr_list)):
            expr_list[i] = expr_list[i].split('*')

            # Каждый множитель в слагаемом инициализируем
            for j in range(len(expr_list[i])):
                if '.' in expr_list[i][j]:
                    expr_list[i][j] = Float(float(expr_list[i][j]))
                expr_list[i][j] = Integer(int(expr_list[i][j]))

            if len(expr_list[i]) != 1:
                expr_list[i] = Mul(expr_list[i])
            else:
                expr_list[i] = expr_list[i][0]

        if len(expr_list) != 1:
            expr_list = Add(expr_list)
        else:
            expr_list = expr_list[0]

        return expr_list


