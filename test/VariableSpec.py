import unittest


class MyTestCase(unittest.TestCase):

    def assignStub(self, typeAssign: str, typeValue: str) -> str:
        f"""
        {typeAssign} a = {typeValue}
        """

    def test_something(self):
        # Given
        testProg = """
        int prog = 12;
        """

        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
