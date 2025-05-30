# mode_select.py: 모드 선택 화면을 구성하며 Basic 모드 진입 및 로딩 처리를 담당함.

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from basic_game import BasicGameWindow  # Basic 모드 화면 불러오기

class ModeSelectWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        # 전체 화면 레이아웃
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # 상단 아이콘 + 타이틀 구성
        icon_layout = QHBoxLayout()
        self.left_icons = QLabel('♥ ♠')
        self.right_icons = QLabel('♣ ♦')
        self.left_icons.setStyleSheet("color: red; font-size: 18px; padding-right: 8px;")
        self.right_icons.setStyleSheet("color: black; font-size: 18px; padding-left: 8px;")
        self.title = QLabel("SHUFFLE")
        self.title.setStyleSheet("font-size: 22px; font-weight: bold; color: black;")
        self.title.setAlignment(Qt.AlignCenter)

        icon_layout.addWidget(self.left_icons)
        icon_layout.addWidget(self.title)
        icon_layout.addWidget(self.right_icons)

        # Basic 모드 버튼
        self.basic_button = QPushButton("🟩 Basic 모드")
        self.basic_button.setStyleSheet("font-size: 16px; padding: 10px;")
        self.basic_button.clicked.connect(self.start_basic_mode)

        # 레이아웃 배치
        layout.addLayout(icon_layout)
        layout.addWidget(self.basic_button)

        # 로딩 메시지 (처음에는 숨김)
        self.loading_label = QLabel("🃏 카드를 준비 중입니다...", self)
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setStyleSheet("""
            background-color: white;
            border: 2px solid #666;
            padding: 15px;
            font-size: 14pt;
            font-weight: bold;
        """)
        self.loading_label.setFixedSize(300, 80)
        self.loading_label.setGeometry((960 - 300) // 2, (640 - 80) // 2, 300, 80)
        self.loading_label.hide()

        self.setLayout(layout)

    def start_basic_mode(self):
        # 버튼/타이틀 숨기고 로딩 표시
        self.title.hide()
        self.left_icons.hide()
        self.right_icons.hide()
        self.basic_button.hide()
        self.loading_label.show()
        QTimer.singleShot(800, self.open_basic_game)

    def open_basic_game(self):
        # 기존 BasicGameWindow가 있으면 제거
        for i in range(self.stacked_widget.count()):
            widget = self.stacked_widget.widget(i)
            if isinstance(widget, BasicGameWindow):
                self.stacked_widget.removeWidget(widget)
                widget.deleteLater()

        # 새 게임 화면 생성 후 이동
        basic_ui = BasicGameWindow(self.stacked_widget)
        basic_ui.reset_game()
        self.stacked_widget.addWidget(basic_ui)
        self.stacked_widget.setCurrentWidget(basic_ui)

    def showEvent(self, event):
        # 다시 돌아왔을 때 버튼/타이틀 복구
        self.title.show()
        self.left_icons.show()
        self.right_icons.show()
        self.basic_button.show()
        self.loading_label.hide()