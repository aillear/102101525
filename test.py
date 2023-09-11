from Support.Delegate import Delegate


def functionA(name):
    print(f"a {name}")


def functionB(nass):
    print(f"b {nass}")


if __name__ == '__main__':
    delegate = Delegate(functionA)
    delegate('initial with A')
    delegate += functionB

    delegate('add B')

    print('-------------')
    delegate -= functionA
    delegate('Removed A')
