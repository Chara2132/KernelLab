from ui.tui.main_view import KernelLabTUI
from utils.helpers import read_kernel_log_journalctl,filter_logs,extract_timestamps,summarize_logs
from webbrowser import open
import subprocess

def logo()->str:
    return r"""
  _  _                 _    _         _          _             _
 | |/ /   ___   _ __  | |\ | |  ___  | |        | |     __ _  | |
 | ' /   / _ \ | '__| | | \| | / _ \ | |        | |    / _ `| | |__
 | . \   | __/ | |    | | \  | | __/ | |__      | |__ | (_| | | |  \
 |_|\_\  \___| |_|    |_|  \_| \___| |____|     |____| \__,_| |_|__/


"""
if __name__=="__main__":
    number=-1
    lines=read_kernel_log_journalctl()
    while(number!=0):
        print(logo())
        number=int(input("\033[37m1. \033[0m \033[32mGo to the shell\033[0m\t\t\033[37m2. \033[0m \033[32mGo to the documentation\033[0m\n\033[37m3. \033[0m \033[32mRead log files\033[0m\t\t\033[37m4. \033[0m \033[32mExit\033[0m\n\n\033[31mChoose: \033[0m"))
        match(number):
            case 1:
                tui=KernelLabTUI()
                tui.run()
            case 2:
                print("Opening the documentation...")
                open("https://kernel-lab-documentation.netlify.app/")
            case 3:
                number2=-1
                while(number!=0):
                    number2 = int(input(
                        "\033[37m1.\033[0m \033[32mRead kern.log\033[0m\t\t"
                        "\033[37m2.\033[0m \033[32mExtract timeline\033[0m\n"
                        "\033[37m3.\033[0m \033[32mSummarize logs\033[0m\t\t"
                        "\033[37m4.\033[0m \033[32mFilter logs (it needs an keyword)\033[0m\n"
                        "\033[37m5.\033[0m \033[32mExit\033[0m\n\n"
                        "\033[31mChoose: \033[0m"
                    ))

                    match(number2):
                        case 1:
                            for line in lines:
                                print(line)
                        case 2:
                            log = extract_timestamps(lines)
                            for line in log:
                                print(line)
                        case 3:
                            summary = summarize_logs(lines)
                            for key, value in summary.items():
                                print(f"{key.capitalize()}: {value}")
                        case 4:
                            keyword = input("Inserisci la parola chiave da cercare: ")
                            log = filter_logs(lines, keyword)
                            for line in log:
                                print(line)
                        case 5:
                            subprocess.run("clear",shell=True)
                            break
                        case _:
                            print("Unrecognized number, Please enter a valid number")
            case 4:
                subprocess.run("clear",shell=True)
                break
            case _:
                print("Unrecognized number, Please enter a valid number")
