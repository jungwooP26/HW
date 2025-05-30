from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
import random

class JokerCardDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 다이얼로그 제목과 크기 설정
        self.setWindowTitle("조커 카드 선택")
        self.setFixedSize(500, 250)

        # 가로 레이아웃 (카드 배치)
        self.layout = QHBoxLayout()
        self.button_group = []
        self.selected_joker = None

        # 조커 카드 목록
        self.joker_cards = [
            ("무늬 무시", "카드의 무늬를 무시하고 숫자만 판단합니다."),
            ("와일드 카드", "비어 있는 족보 자리를 채워주는 와일드 카드입니다."),
            ("+10 부스트", "2,3,4,5 카드에 각각 +10점을 부여합니다."),
            ("더블 점수", "이번 턴의 점수를 2배로 만듭니다."),
            ("라운드 x0.5", "라운드 수 + 0.5 배수 적용."),
            ("고정 10점", "선택한 모든 카드의 가치를 10으로 고정합니다."),
            ("남은턴 x1.25", "남은 턴 수 X 1.25 배수 적용."),
            ("랜덤 효과", "카드 가중치에 +1, +10, +100 또는 -10 등의 랜덤 효과 적용."),
            ("그림카드 x3", "모든 카드가 J/Q/K일 경우 3배 점수 적용."),
            ("가중치 재계산", "카드 가중치를 2번 더 계산하여 총 3회 계산.")
        ]

        # 무작위 3장 선택
        selected = random.sample(self.joker_cards, 3)

        for name, tooltip in selected:
            btn = QPushButton(name)
            btn.setFixedSize(120, 180)
            btn.setToolTip(tooltip)
            btn.setStyleSheet(self.default_style())
            btn.clicked.connect(lambda _, b=btn, n=name: self.select_joker(b, n))
            self.layout.addWidget(btn)
            self.button_group.append(btn)

        # 닫기 버튼
        close_btn = QPushButton("확인")
        close_btn.clicked.connect(self.confirm_selection)

        # 전체 레이아웃
        vbox = QVBoxLayout()
        vbox.addLayout(self.layout)
        vbox.addWidget(close_btn, alignment=Qt.AlignCenter)
        self.setLayout(vbox)

    def default_style(self):
        return """
            QPushButton {
                font-size: 12px;
                font-weight: bold;
                color: black;
                border: 2px solid black;
                border-radius: 8px;
                background-color: white;
            }
            QPushButton:hover {
                border: 3px solid blue;
                background-color: #f0f8ff;
            }
        """

    def selected_style(self):
        return """
            QPushButton {
                font-size: 12px;
                font-weight: bold;
                color: white;
                border: 3px solid darkblue;
                border-radius: 8px;
                background-color: #4169e1;
            }
        """

    def select_joker(self, button, name):
        # 모든 버튼 초기화
        for btn in self.button_group:
            btn.setStyleSheet(self.default_style())

        # 선택된 버튼 강조
        button.setStyleSheet(self.selected_style())
        self.selected_joker = name

    def confirm_selection(self):
        if self.selected_joker is None:
            QMessageBox.warning(self, "선택 안 됨", "조커 카드를 하나 선택해주세요.")
        else:
            self.accept()  # 창 닫고 선택 완료