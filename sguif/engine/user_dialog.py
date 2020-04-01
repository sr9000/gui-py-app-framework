from PyQt5.QtWidgets import QMainWindow, QMessageBox


def yes_no_dialog(mwnd: QMainWindow, question: str) -> bool:
    return QMessageBox.Yes == QMessageBox.question(mwnd, '', question,
                                                   QMessageBox.Yes | QMessageBox.No,
                                                   QMessageBox.Yes)


def info_dialog(mwnd: QMainWindow, message: str) -> None:
    QMessageBox.information(mwnd, '', message, QMessageBox.Ok, QMessageBox.Ok)


def warning_dialog(mwnd: QMainWindow, message: str) -> None:
    QMessageBox.warning(mwnd, '', message, QMessageBox.Ok, QMessageBox.Ok)


def error_dialog(mwnd: QMainWindow, message: str) -> None:
    QMessageBox.critical(mwnd, '', message, QMessageBox.Ok, QMessageBox.Ok)
