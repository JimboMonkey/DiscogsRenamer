import sys

from PyQt6.QtWidgets import QApplication


# Start the application
def main():
    application = QApplication(sys.argv)

    sys.exit(application.exec())


if __name__ == "__main__":
    main()
