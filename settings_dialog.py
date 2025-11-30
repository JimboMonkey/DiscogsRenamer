from gui.settings_dialog_gui import SettingsDialogGui


class SettingsDialog:

    def __init__(self) -> None:

        self._ui = SettingsDialogGui()

        self._init_connections()

    def show(self) -> None:
        self._ui.exec()  # only run modal loop when explicitly asked

    # Link GUI widgets to the functions
    def _init_connections(self) -> None:
        self._ui.close_button.clicked.connect(self._ui.close_dialog)

    def get_filename_format(self) -> str:
        return self._ui.format_lineedit.text()
