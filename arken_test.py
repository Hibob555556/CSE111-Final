from sel_tools import AutoTest, Parser
from e2e_tests import *
import threading
from threading import Thread
from logger import logger
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import os
from PIL import Image

RES_FILE_DIR = "e2e_results/"
lgr = logger()

class ArkenTest:
    def main():
        # run tests
        if threading.active_count() < 2:
            thread = Thread(target = ArkenTest.run_suite)
            thread.start()
            return "Started"
        else:
            return "Busy"


    def gen_results():
        files = Parser.get_unique_files()
        results = []
        for file in files:
            json_res = ""
            with open(f"{RES_FILE_DIR}{file}", "r+", encoding="utf-8") as res_file:
                json_res = res_file.readlines()
            results.append(json_res)

        total_tests        = Parser.get_test_count(results)
        total_steps        = Parser.get_step_count(results)
        success_count      = Parser.get_success_count(results)
        step_success_count = Parser.get_step_success_count(results)
        fail_count         = Parser.get_fail_count(results)
        step_fail_count    = Parser.get_step_fail_count(results)
        percentage_passed  = Parser.get_test_percentage(results)

        ArkenTest.gen_suite_graphs(total_tests, total_steps, success_count, step_success_count, 
                                   fail_count, step_fail_count, percentage_passed)
        return 1

    
    def gen_suite_graphs(total_tests: int, total_steps: int, success_count: int, 
                         step_success_count: int, fail_count: int, 
                         step_fail_count: int, percentage_passed: float):
        ArkenTest.gen_bar_chart(success_count,fail_count)
        return 1


    @staticmethod
    def gen_bar_chart(success_count, fail_count):
        fig, ax = plt.subplots()
        results = ['Passed', 'Failed'] 
        colors  = ['green', 'red']
        vals    = [success_count, fail_count]
        
        ax.bar(results, vals, color=colors)
        ax.set_ylabel('Test Count')
        ax.set_xlabel('Result')
        ax.set_title('Successful Vs Failed Tests')
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        
        if os.path.exists('img_results') == False:
            os.mkdir('img_results')
        plt.savefig('pass_fail_bar.png')

        orig_image = Image.open("pass_fail_bar.png")
        new_size = (360,270)
        new_image = orig_image.resize(new_size)
        new_image.save("pass_fail_bar.png")


    @staticmethod
    def run_suite():
        # create auto test instance
        at = AutoTest()

        # run tests
        test_page_nav(at)
        test_number_input(at)
        test_with_failure(at)

        at.dispose()
        return 1