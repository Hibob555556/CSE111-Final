from selenium.webdriver.chrome.service import Service
from sel_tools import AutoTest, at_expect

def test_page_nav(at: AutoTest):
    test_case = at.TestCase("Page Navigation", 1, at)
    driver = at.driver
    test_case.driver = driver 
    expect = at_expect(driver)
    test_case.start_test_case()

    #region Step 1
    # navigate to google.com
    test_case.curr_step = 1
    at.navigate("https://www.google.com/")
    res = expect.url_to_be("https://www.google.com", False)
    test_case.record_step(res,"Navigate To https://www.google.com")
    #endregion

    test_case.save_results()


def test_number_input(at: AutoTest):
    test_case = at.TestCase("Number Inputs", 3, at)
    driver = at.driver
    test_case.driver = driver 
    expect = at_expect(driver)
    test_case.start_test_case()

    BASE_URI = "https://the-internet.herokuapp.com/"

    #region Step 1
    # The app should load
    test_case.curr_step = 1
    at.navigate(BASE_URI)
    res = expect.url_to_be(BASE_URI)
    test_case.record_step(res,"The app should load.")
    #endregion

    #region Step 2
    # The page should load
    test_case.curr_step = 2
    at.click("//ul//li/a[text()=\"Inputs\"]")
    res = expect.url_to_be(f"{BASE_URI}inputs")
    test_case.record_step(res,"The inputs page should load.")
    #endregion

    #region Step 3
    # The input should allow numbers
    test_case.curr_step = 3
    input_elem = "//*[@id=\"content\"]/div/div/div/input"
    at.set_value(input_elem,123)
    res = expect.val_to_be(input_elem,123)
    test_case.record_step(res,"The input should allow numbers")
    #endregion

    test_case.save_results()


def test_with_failure(at: AutoTest):
    test_case = at.TestCase("Fail Test", 1, at)
    driver = at.driver
    test_case.driver = driver
    expect = at_expect(driver)
    test_case.start_test_case

    BASE_URI = "https://the-internet.herokuapp.com/"

    #region Step 1
    # the inputs page should load
    test_case.curr_step = 1
    at.navigate(BASE_URI)
    res = expect.url_to_be(f"{BASE_URI}inputs")
    test_case.record_step(res,"The inputs page should load")
    #endregion

    test_case.save_results()