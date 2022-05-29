from datetime import datetime


class Logger:
    @staticmethod
    def get_time():
        return datetime.now().strftime("%H:%M:%S")

    def log(self, message, scope="App"):
        print(f"{self.get_time()} | [{scope}] {message}")


logger = Logger()
