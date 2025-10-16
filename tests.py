import pytest
from sel_tools import *


def test_at():
    driver = AutoTest.gen_test_driver()
    at = driver
    _test_get_text(at)
    _test_get_value(at)
    _test_get(at)

def _test_get_text(a):
    a.navigate("https://the-internet.herokuapp.com/")
    txt = a.get_text("//*[@id='content']/h1")
    assert txt == "Welcome to the-internet"

def _test_get_value(a):
    a.click('//*[@id="content"]/ul/li[27]/a')
    val1 = a.get_value("//*[@id='content']/div/div/div/input")
    a.set_value("//*[@id='content']/div/div/div/input", 123)
    val2 = a.get_value("//*[@id='content']/div/div/div/input")
    assert val1 == ''
    assert val2 == '123'


def _test_get(a):
    a.click('//*[@id="content"]/ul/li[27]/a')
    val1 = a.get_value("//*[@id='content']/div/div/div/input")
    a.set_value("//*[@id='content']/div/div/div/input", 123)
    val2 = a.get_value("//*[@id='content']/div/div/div/input")
    assert val1 == ''
    assert val2 == '123'



# Call the main function that is part of pytest so that the
# computer will execute the test functions in this file.
pytest.main(["-v", "--tb=line", "-rN", __file__])
