import os
from pathlib import Path

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication

from gui.icon_loader import icon_path, load_pixmap


def test_window_control_icons_render_without_deleted_png_assets():
    app = QApplication.instance() or QApplication([])

    for name in (
        "window/close_winow.svg",
        "window/full_window.svg",
        "window/hide_window.svg",
    ):
        pixmap = load_pixmap(icon_path(name), 40)
        assert not pixmap.isNull()
        assert pixmap.width() > 0
        assert pixmap.height() > 0

    assert app is not None


def test_icons_in_purpose_folders_are_loadable():
    app = QApplication.instance() or QApplication([])
    icons_dir = Path(__file__).parents[1] / "gui" / "assets" / "icons"
    icon_paths = tuple(icons_dir.rglob("*.svg"))

    assert icon_paths
    for path in icon_paths:
        relative_path = path.relative_to(icons_dir).as_posix()
        assert not load_pixmap(icon_path(relative_path), 24).isNull()

    assert app is not None


def test_missing_icon_path_is_reported():
    missing_path = Path(__file__).parent / "missing-icon.svg"

    with pytest.raises(FileNotFoundError):
        load_pixmap(missing_path, 20)
