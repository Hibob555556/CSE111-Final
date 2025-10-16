import datetime

class logger:
    def __init__(self):
        pass


    def info(self,message):
        colors = self.colors()
        date = self._get_time()
        print(f"{date}{colors.YELLOW} > {message}{colors.RESET}")


    def error(self,message):
        colors = self.colors()
        date = self._get_time()
        print(f"{date}{colors.RED} >> {message}{colors.RESET}")


    def success(self,message):
        colors = self.colors()
        date = self._get_time()
        print(f"{date}{colors.GREEN} >> {message}{colors.RESET}")

    
    def working(self,message):
        colors = self.colors()
        date = self._get_time()
        print(f"{date}{colors.BLUE} > {message}{colors.RESET}")


    def debug(self,message):
        colors = self.colors()
        date = self._get_time()
        print(f"{date}{colors.PURPLE} >>> DEBUG | {message}{colors.RESET}")


    def warn(self,message):
        colors = self.colors()
        date = self._get_time()
        print(f"{date}{colors.ORANGE} >> {message}{colors.RESET}")


    @staticmethod
    def _get_time():
        curr_date = datetime.datetime.now()
        curr_date = curr_date.strftime('%d-%m %H:%M:%S.%f')[:-3]
        formatted_time = f"[{curr_date}]"
        return formatted_time


    class colors:
        def __init__(self):
            self.GREEN  = "\033[0;32m"
            self.RED    = "\033[0;31m"
            self.BLUE   = "\033[0;34m"
            self.YELLOW = "\033[1;33m"
            self.PURPLE = "\033[0;35m"
            self.ORANGE = "\033[38:5:166m"
            self.RESET  = "\033[0m"