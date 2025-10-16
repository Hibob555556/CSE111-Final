import pytest
from sel_tools import *

@pytest.fixture(scope="session")
def at():
    return AutoTest()

def test_at(at):
    def test_get_text(at):
        at.navigate("https://the-internet.herokuapp.com/")
        txt = at.get_text("//*[@id='content']/h1")
        assert txt == "Welcome to the-internet"

    def test_get_value(at):
        at.click('//*[@id="content"]/ul/li[27]/a')
        val1 = at.get_value("//*[@id='content']/div/div/div/input")
        at.set_value("//*[@id='content']/div/div/div/input", 123)
        val2 = at.get_value("//*[@id='content']/div/div/div/input")
        assert val1 == ''
        assert val2 == '123'

    test_get_text(at)
    test_get_value(at)
    

# Call the main function that is part of pytest so that the
# computer will execute the test functions in this file.
pytest.main(["-v", "--tb=line", "-rN", __file__])
