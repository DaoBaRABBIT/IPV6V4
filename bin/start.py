import sys
try:
    sys.path.append('.')
    from core import main
except:
    sys.path.append('..')
    from core import main


class openmain():
    def __init__(self):
        main.mianGUI()

if __name__ == '__main__':
    start = openmain()
