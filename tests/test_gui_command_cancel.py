import os
import threading
from unittest.mock import Mock, patch

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication

from gui.main_window import CommandWorker, MainWindow


@pytest.fixture(scope="module")
def qt_app():
    return QApplication.instance() or QApplication([])


class CancelCommand:
    def __init__(self):
        self.pending_app = None
        self.pending_file = None
        self.pending_learning_candidate = None

    @staticmethod
    def is_cancel_action(text: str) -> bool:
        return text.strip().casefold() == "скасувати"

    def cancel_pending_action(self, silent: bool = False) -> None:
        _ = silent
        self.pending_app = None
        self.pending_file = None
        self.pending_learning_candidate = None


def test_cancel_message_interrupts_busy_gui_command(qt_app):
    window = MainWindow(command=CancelCommand())
    cancel_event = threading.Event()
    window._command_busy = True
    window._command_cancel_event = cancel_event

    with patch("gui.main_window.interrupt_voice") as interrupt_voice:
        window.send_message("скасувати")

    assert cancel_event.is_set()
    interrupt_voice.assert_called_once_with()
    assert window._command_busy
    window.close()


def test_cancelled_worker_does_not_start_command_and_reports_cancellation():
    command = Mock()
    cancel_event = threading.Event()
    cancel_event.set()
    worker = CommandWorker(command, "довга команда", cancel_event=cancel_event)
    outputs = []
    worker.signals.finished.connect(lambda _text, output: outputs.append(output))

    worker.run()

    command.process_recognized_command.assert_not_called()
    assert outputs == ["Команду скасовано."]


def test_cancel_requested_as_command_finishes_clears_pending_action(qt_app):
    command = CancelCommand()
    command.pending_file = {"awaiting_target": True}
    window = MainWindow(command=command)
    window._command_busy = True
    window._command_cancel_event = threading.Event()
    window._command_cancel_event.set()

    window._command_finished("Знайди файл", "Вкажіть назву файла.")

    assert command.pending_file is None
    assert not window._command_busy
    window.close()
