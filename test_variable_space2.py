

from Const import Const
from test_variable_space import test_variable

def test_variable2():
    const = Const()
    const['pi2'] = 2
    print(const['pi2'])
    test_variable()




def test():
    w = test_variable2()



if __name__ == "__main__":
    test()