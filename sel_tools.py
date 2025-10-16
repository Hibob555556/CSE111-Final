from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By
from selenium import webdriver
from logger import *
import json
import requests
import zipfile
import shutil
import csv
import os

lgr = logger()

class AutoTest:
#region Selenium 
    def __init__(self):
        self.driver: webdriver = self.gen_test_driver()
        
        
    def get_driver(self):
        return self.driver
    

    @staticmethod
    def gen_test_driver():
        '''
        ## Description: 
        Generates and returns an instance of chromedriver which will be used to control each step.

        ## Returns:

        '''
        # store base uri of chromedriver api
        base_uri = "https://storage.googleapis.com/chrome-for-testing-public"

        # get the latest version
        lgr.info("Getting latest version of chromedriver")
        res = requests.get("https://versionhistory.googleapis.com/v1/chrome/platforms/win/channels/stable/versions")
        version = res.json()["versions"][0]["version"]

        # build request and download latest version
        lgr.info("Downloading latest chromedriver")
        request = f"{base_uri}/{version}/win64/chromedriver-win64.zip"
        res = requests.get(request)

        # write the file to disk and unzip it
        lgr.info("Extracting chromedriver")
        open("./tmp_download.zip", 'wb').write(res.content)
        with zipfile.ZipFile("./tmp_download.zip", 'r') as zip_ref:
            zip_ref.extractall()

        # Move files into known location
        lgr.info("Organizing chromedriver files")
        shutil.move(os.path.join(os.curdir,'chromedriver-win64/chromedriver.exe'), os.path.join(os.curdir,'driver/chromedriver.exe'))
        shutil.move(os.path.join(os.curdir,'chromedriver-win64/LICENSE.chromedriver'), os.path.join(os.curdir,'driver/license/LICENSE.chromedriver'))
        shutil.move(os.path.join(os.curdir,'chromedriver-win64/THIRD_PARTY_NOTICES.chromedriver'), os.path.join(os.curdir,'driver/license/THIRD_PARTY_NOTICES.chromedriver'))

        lgr.info("Removing tmp files")
        os.remove("tmp_download.zip")

        # build the path to the driver
        d_path = os.path.join(os.curdir,"driver/chromedriver.exe")

        # create a service to manage driver processes
        lgr.info("Generating chromedriver service with downloaded driver")
        service = Service(executable_path=d_path)

        # create an instance of chrome
        lgr.info("Creating chromedriver instance")
        driver = webdriver.Chrome(service=service)
        return driver

    def dispose(self):
        self.driver.quit()
#endregion

#region Test Control
    def navigate(self, url: str):
        '''
        ## Description:
        Navigates to the website specified with <i>url</i> in the active browser.
        '''
        self.driver.get(url)

    def click(self, element: str):
        elem = self.driver.find_element(By.XPATH, element)
        elem.click()

    def set_value(self, element: str, val: any):
        elem = self.driver.find_element(By.XPATH, element)
        elem.send_keys(val)

    def get_value(self, element: str):
        elem = self.driver.find_element(By.XPATH, element)
        val = elem.get_attribute('value')
        return val

    def get_text(self, element: str):
        elem = self.driver.find_element(By.XPATH, element)
        txt = elem.text
        return txt

#endregion

#region Test Case Object
    class TestCase:
        def __init__(self, test_name, step_count, driver: webdriver):
            self.test_name = test_name
            self.step_count = step_count
            self.step_names = [""] * step_count
            self.step_results = [False] * step_count
            self.driver: webdriver = driver
            self.curr_step = 0


        def record_step(self, result: bool, name: str):
            '''
            ## Description:
            Records the results of the current step. This is the last thing that should be called in any step. 
            <br><br>
            ## Notes:
            Once this has been called the step will be added into the results csv file when you call <i>save_results()</i> at the end of your test
            '''
            self.step_names[self.curr_step - 1] = name
            self.step_results[self.curr_step - 1] = result


        def check_url(self, expected, exact=True):
            '''
            ## Description:
            Check the current page URL against the provided URL.
            <br><br>
            ## Notes:
            Use of the optional <i>exact</i> parameter allows you to match parts of a url. 
            i.e. if you are on hxxp://example.com/page you can match with hxxp://example.com/
            allowing you to match dynamic or large URL's without knowing the entire thing. 
            <br><br>
            ## Arguments
            - expected: str
            - exact: boolean (optional)
            <br><br>
            ## Returns
            - boolean
            '''
            url = self.driver.current_url
            try:
                if exact:
                    assert url == expected
                else:
                    assert expected in url
            except AssertionError:
                lgr.error(f"Expected: {expected} received: {url}")
                return False
            else:
                sign = "==" if exact else "~"
                lgr.success(f"Success: {expected} {sign} {url}")
                return True

        
        def save_results(self):
            '''
            ## Description: 
            Save the results of the current test into a csv file
            '''
            # ensure results folder exists
            # create it if it does not exist
            lgr.info("Checking if results folder exists")
            res_path = "./e2e_results/"
            if os.path.exists(res_path) == False:
                lgr.error("Results folder not found")
                lgr.info("Creating results folder")
                try: 
                    os.mkdir(res_path)
                except Exception as err:
                    lgr.error("Could not generate results folder")
                    return
                else:
                    lgr.success("Created results folder")

            # generate file name
            lgr.info("Generating file name")
            name = self.test_name.replace(" ", "_")
            file_name = f"{res_path}{name}.json"

            # record results to write to file
            lgr.info("Compiling results")

            results = {
                "test_name":    self.test_name,
                "step_count":   self.step_count,
                "step_names":   self.step_names,
                "step_results": self.step_results
            }

            json_results = json.dumps(results)

            # write results file
            lgr.info("Writing file")
            try:
                with open(file_name, "w+", newline='') as res_file:
                    res_file.writelines(json_results)
            except Exception as err:
                lgr.error(f"Could not create results file: {err}")
            else:
                lgr.success("Successfully created results file")


        def start_test_case(self):
            lgr.working(f"Starting test case: {self.test_name}")
#endregion

#region Expect Functions
class at_expect(AutoTest):
    def __init__(self,driver):
        self.driver = driver

    def url_to_be(self,expected,exact=True):
        '''
        ## Description:
        Check the current page URL against the provided URL.
        <br><br>
        ## Notes:
        Use of the optional <i>exact</i> parameter allows you to match parts of a url. 
        i.e. if you are on hxxp://example.com/page you can match with hxxp://example.com/
        allowing you to match dynamic or large URL's without knowing the entire thing. 
        <br><br>
        ## Arguments
        - expected: str
        - exact: boolean (optional)
        <br><br>
        ## Returns
        - boolean
        '''
        url = self.driver.current_url
        try:
            if exact:
                assert url == expected
            else:
                assert expected in url
        except AssertionError:
            lgr.error(f"Expected: {expected} received: {url}")
            return False
        else:
            sign = "==" if exact else "~"
            lgr.success(f"Assertion success: {expected} {sign} {url}")
            return True
        

    def val_to_be(self,element,expected):
        elem = self.driver.find_element(By.XPATH,element)
        val = elem.get_attribute('value')
        try:
            assert val == str(expected)
        except AssertionError as err:
            lgr.error(f"Expected: {expected} received: {val}")
            lgr.error(f"Stacktrace: {err}")
            return False
        else:
            lgr.success(f"Assertion success {expected} == {val}")
            return True
#endregion

#region Result Parsing
class Parser:
    def get_unique_files():
        '''
        Description: returns a list of all files within the ./e2e_results/ directory

        Returns
          - files: list
        '''
        # specify results path. Create if it does not exist
        res_path = "./e2e_results/"
        if os.path.exists(res_path) == False:
            lgr.warn("Results Not Found")
            return "Results Not Found"
        else:
            # get contents of directory
            dir_contents = os.listdir(res_path)
            files = []

            # add all files in directory to files list
            for item in dir_contents:
                if os.path.isfile(f"{res_path}{item}"):
                    files.append(item)
            # return a list of all files in the ./e2e_results/ directory
            return files    
        

    def get_test_count(json_res: list):
        '''
        Description: Returns the number of tests which are recorded in the ./e2e_results/ directory

        Returns
          - count: Int
        '''
        count = len(json_res)
        return count
    

    def get_step_count(json_res: list):
        '''
        Description: Returns the number of test steps which are recorded in the ./e2e_results/ directory

        Returns
          - count: Int
        '''
        count = 0
        for res in json_res:
            json_str = json.loads(res[0])
            count += json_str["step_count"]
        return count
    

    def get_success_count(json_res: list):
        '''
        Description: Returns the number of tests which succeeded 

        Returns:
          - count: Int
        '''
        count = 0
        for res in json_res:
            json_str = json.loads(res[0])
            if "False" not in str(json_str["step_results"]):
                count += 1
        return count
    

    def get_step_success_count(json_res: list):
        '''
        Description: Returns the number of tests which succeeded 

        Returns:
          - count: Int
        '''
        count = 0
        for res in json_res:
            json_str = json.loads(res[0])["step_results"]
            for entry in json_str:
                if entry:
                    count += 1
        return count
    

    def get_fail_count(json_res: list):
        '''
        Description: Returns the number of tests which failed

        Returns:
          - count: Int
        '''
        count = 0
        for res in json_res:
            json_str = json.loads(res[0])
            if "False" in str(json_str["step_results"]):
                count += 1
        return count
            

    def get_step_fail_count(json_res: list):
        '''
        Description: Returns the number of tests which failed 

        Returns:
          - count: Int
        '''
        count = 0
        for res in json_res:
            json_str = json.loads(res[0])["step_results"]
            for entry in json_str:
                if not entry:
                    count += 1
        return count


    def get_test_percentage(json_res: list):
        '''
        Description: Returns the percentage of tests which passed

        Returns:
          - count: Int
        '''
        success_count = Parser.get_success_count(json_res)
        failed_count  = Parser.get_fail_count(json_res)
        total = success_count + failed_count
        success_percentage = (success_count / total) * 100
        return success_percentage
#endregion
