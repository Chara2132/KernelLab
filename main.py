from rich import print
from core.log_parser import read_kernel_log

def main()->None:
    for line in read_kernel_log()[:10]:
        print(line)

if __name__=="__main__":
    main()