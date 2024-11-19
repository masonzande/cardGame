class I:
    def some_unrelated_func(self):
        print("I")

class A:
    field1: int
    def __init__(self):
        self.field1 = 0

class B(A, I):
    field2: int
    def __init__(self, field2):
        self.field2 = field2
        super().__init__()

class C(B):
    def __init__(self, component_of_field2, other_field):
        super().__init__(other_field * component_of_field2)
        

if __name__ == "__main__":
    print(C(2, 3).field1)