from ui.tui.main_view import KernelLabTUI
from utils.helpers import read_log_file,filter_logs,extract_timestamps,summarize_logs
from webbrowser import open
def logo()->str:
    return r"""
  _  _                 _    _         _          _             _
 | |/ /   ___   _ __  | |\ | |  ___  | |        | |     __ _  | |
 | ' /   / _ \ | '__| | | \| | / _ \ | |        | |    / _ `| | |__
 | . \   | __/ | |    | | \  | | __/ | |__      | |__ | (_| | | |  \
 |_|\_\  \___| |_|    |_|  \_| \___| |____|     |____| \__,_| |_|__/


"""
    #128,129,132,133



if __name__=="__main__":
    print(logo())
    number=-1
    while(number!=0):
        number=input("\033[37m1. \033[0m \033[32mGo to the shell\033[0m\t\t\033[37m2. \033[0m \033[32mGo to the documentation\033[0m\n\033[37m3. \033[0m \033[32mRead log files\033[0m\t\t\033[37m4. \033[0m \033[32mExit\033[0m\n\n\033[31mChoose: \033[0m")
        match(number):
            case 1:
                tui=KernelLabTUI()
                tui.run()
            case 2:
                pass