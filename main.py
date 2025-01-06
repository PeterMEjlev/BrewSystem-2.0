import sys
from PyQt5.QtWidgets import QApplication
from Screens.Brewscreen.brewscreen import FullScreenWindow

def main():
    app = QApplication(sys.argv)
    window = FullScreenWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
