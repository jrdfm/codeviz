class TestClass:
    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value

if __name__ == "__main__":
    obj = TestClass(42)
    print(obj.get_value()) 