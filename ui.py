from tkinter import Frame, Label, Button
from arken_test import ArkenTest
from PIL import Image, ImageTk
from logger import logger
import tkinter as tk
import threading

lgr = logger()

class ArkenTestUI:
    def main():
        ArkenTestUI.run_ui()


    @staticmethod
    def run_ui():
        root = tk.Tk()
        ArkenTestUI.set_window_size(root,400,400)
        frm_main = Frame(root)
        frm_main.master.title("ArkenTest")
        frm_main.pack(padx=5,pady=5,fill=tk.BOTH,expand=True)
        ArkenTestUI.pop_ui(frm_main)
        frm_main.mainloop()


    @staticmethod
    def pop_ui(frm):
        # components for use in running automated tests
        lbl_run_tests = Label(frm,text="Run Automated Tests")
        lbl_run_tests.grid(row=0,column=0,padx=5,pady=5)
        run_btn = Button(frm,text="Run",width=10)
        run_btn.grid(row=0,column=1,padx=5,pady=5)
        lbl_msg = Label(frm,text="")
        lbl_msg.grid(row=0,column=3,padx=5,pady=5)

        # components for use in generating test results
        lbl_gen_res = Label(frm,text="Generate Test Results")
        lbl_gen_res.grid(row=1,column=0,padx=5,pady=5)
        gen_btn = Button(frm,text="Generate",width=10)
        gen_btn.grid(row=1,column=1,padx=5,pady=5)
        

        def reset_text():
            '''
            Description: reset the text of the auto test msg from "running" to "" and reactivate run button
            '''
            lbl_msg.config(text="")
            run_btn["state"] = "active"


        def active_text():
            '''
            Description: This function monitors the progress of the automated tests and resets the text and 
                         button once testing is finished
            '''
            # set the label next to the button to indicate the tests are running
            lbl_msg.config(text="Running")

            # This program will run on 2 threads, if we are greater than that, the tests are running
            if threading.active_count() > 2:
                # repeat until the tests are finished
                timer = threading.Timer(2.0,active_text)
                timer.start()
            else:
                # clear the text next to the button
                reset_text()


        def run_auto_tests():
            '''
            Description: This function disables the run button, triggers the automated tests, sets the text next
                         to the button to reflect that testing is in progress, triggers a function to monitor
                         the progress of the testing.
            '''
            # disable the run button
            run_btn["state"] = "disabled"

            # set the text to started or busy
            text = ArkenTest.main()
            lbl_msg.config(text=text)

            # after 2 seconds trigger the active_text function
            timer = threading.Timer(2.0,active_text)
            timer.start()


        def gen_suite_results():
            '''
            Description: This function will generate test suite results based on the json files in the e2e_results directory
            '''
            # generate the test suite results and store the success result
            res = ArkenTest.gen_results()

            # if the results were successfully created display the graph
            if res == 1:
                image1 = Image.open("pass_fail_bar.png")
                test = ImageTk.PhotoImage(image1)
                label1 = Label(image=test)
                label1.image = test
                label1.place(x=0,y=80)


        # configure the run_btn button to run the Selenium auto tests
        run_btn.config(command=run_auto_tests)


        # configure the gen_btn to generate and display test results
        gen_btn.config(command=gen_suite_results)

        
    @staticmethod
    def set_window_size(root: tk, x: int, y: int):
        root.geometry(f"{x}x{y}")


if __name__ == "__main__":
    ArkenTestUI.main()
