from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout

from ..icon_loader import load_pixmap


# ============================ КАРТКА ПОВІДОМЛЕННЯ ЧАТУ ============================
class ChatCard(QFrame):
    """A message card used as a visual placeholder in the prototype."""

    def __init__(
        self,
        author: str,
        body: str,
        time: str,
        icon: str,
        is_user: bool = False,
        status: str | None = None,
        status_icon: str | None = None,
    ) -> None:
        super().__init__()
        self.setObjectName("userCard" if is_user else "assistantCard")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 10)
        layout.setSpacing(12)

        # Ліва частина картки: аватар асистента або користувача.
        icon_label = QLabel()
        icon_label.setObjectName("cardIcon")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setFixedSize(28, 28)
        if icon.lower().endswith((".svg", ".png")):
            icon_label.setPixmap(load_pixmap(icon, 20))
        else:
            icon_label.setText(icon)
        layout.addWidget(icon_label, 0, Qt.AlignmentFlag.AlignTop)

        # Права частина картки: заголовок, текст і час.
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        author_label = QLabel(author)
        author_label.setObjectName("messageAuthor")
        header_layout.addWidget(author_label)
        header_layout.addStretch()

        # Необов'язковий рядок статусу праворуч у заголовку картки.
        if status:
            if status_icon:
                status_icon_label = QLabel()
                status_icon_label.setFixedSize(16, 16)
                status_icon_label.setPixmap(load_pixmap(status_icon, 14))
                header_layout.addWidget(status_icon_label)

            status_label = QLabel(status)
            status_label.setObjectName("messageStatus")
            status_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            header_layout.addWidget(status_label)

        text_layout.addLayout(header_layout)

        body_label = QLabel(body)
        body_label.setObjectName("messageBody")
        body_label.setWordWrap(True)
        text_layout.addWidget(body_label)

        time_label = QLabel(time)
        time_label.setObjectName("messageTime")
        text_layout.addWidget(time_label)

        layout.addLayout(text_layout, 1)
