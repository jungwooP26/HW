# basic_game.py: Basic 모드의 카드 선택, 족보 판별, 점수 계산 등 게임 핵심 로직을 구현함.

from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
    QMessageBox, QGraphicsOpacityEffect, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation
import random

from joker_dialog import JokerCardDialog  # 조커 카드 선택 창 import
from utils import calculate_score  # 점수 계산 함수 import

class BasicGameWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget  # 메인으로 돌아가기 위한 스택 위젯
        self.phase = 1  # 현재 선택 단계 (1단계 또는 2단계)
        self.selected_cards = []  # 선택된 최종 5장의 카드 저장
        self.upper_buttons = []  # 1단계 카드 버튼
        self.lower_buttons = []  # 2단계 카드 버튼
        self.selected_joker = None  # 선택된 조커 카드 저장

        # 상단 안내 라벨
        self.info_label = QLabel("1단계: 카드 4장에서 3장 선택")

        # 선택 완료 버튼
        self.confirm_btn = QPushButton("\ud83d\udd12 선택 완료")
        self.confirm_btn.setEnabled(False)
        self.confirm_btn.clicked.connect(self.confirm_selection)

        # 조커 카드 보기 버튼
        self.joker_btn = QPushButton("\ud83b\udcc1 조커 카드 보기")
        self.joker_btn.clicked.connect(self.show_joker_cards)

        # 메인으로 돌아가기 버튼
        self.back_btn = QPushButton("\ud83d\udd19 메인으로")
        self.back_btn.clicked.connect(self.go_back)

        # 카드 버튼 배치용 레이아웃
        self.upper_layout = QHBoxLayout()
        self.lower_layout = QHBoxLayout()

        self.generate_cards(self.upper_layout, self.upper_buttons, 4)  # 1단계 카드 생성

        # 상단 UI 배치
        top = QHBoxLayout()
        top.addWidget(self.info_label)
        top.addStretch()
        top.addWidget(self.back_btn)

        # 전체 UI 배치
        layout = QVBoxLayout()
        layout.addLayout(top)
        layout.addLayout(self.upper_layout)
        layout.addSpacing(20)
        layout.addLayout(self.lower_layout)
        layout.addWidget(self.confirm_btn)
        layout.addWidget(self.joker_btn)
        self.setLayout(layout)

    def reset_game(self):
        # 게임 상태 초기화
        self.phase = 1
        self.selected_cards.clear()
        self.upper_buttons.clear()
        self.lower_buttons.clear()
        self.selected_joker = None
        self.info_label.setText("1단계: 카드 4장에서 3장 선택")
        self.confirm_btn.setEnabled(False)

        # 기존 카드 제거
        while self.upper_layout.count():
            item = self.upper_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        while self.lower_layout.count():
            item = self.lower_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.upper_layout = QHBoxLayout()
        self.lower_layout = QHBoxLayout()

        self.generate_cards(self.upper_layout, self.upper_buttons, 4)
        self.layout().insertLayout(1, self.upper_layout)
        self.layout().insertLayout(3, self.lower_layout)

    def generate_cards(self, layout, buttons, count):
        # 카드 무작위 생성 및 UI 버튼으로 생성
        suits = ['\u2665', '\u2660', '\u2666', '\u2663']  # ♥, ♠, ♦, ♣
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        for _ in range(count):
            suit = random.choice(suits)
            rank = random.choice(ranks)
            card_text = f"{suit} {rank}"
            color = "red" if suit in ['\u2665', '\u2666'] else "black"

            btn = QPushButton(card_text)
            btn.setFixedSize(100, 150)
            btn.setCheckable(True)
            btn.clicked.connect(self.update_selection)
            btn.setStyleSheet(f"""
                QPushButton {{
                    font-size: 20px;
                    font-weight: bold;
                    color: {color};
                    border: 2px solid black;
                    border-radius: 8px;
                    background-color: white;
                }}
                QPushButton:checked {{
                    border: 3px solid blue;
                    background-color: #f0f8ff;
                }}
            """)
            layout.addWidget(btn)
            buttons.append(btn)

    def update_selection(self):
        # 카드 선택 시 상태 업데이트 및 족보 안내 표시
        if self.phase == 1:
            sel = [b for b in self.upper_buttons if b.isChecked()]
            self.confirm_btn.setEnabled(len(sel) > 0)
            if len(sel) >= 2:
                score_info = calculate_score(sel, self.selected_joker)
                self.info_label.setText(
                    f"1단계 선택 중 | 족보: {score_info['combo_name']} | 가치합: {score_info['value_sum']} | 배수: x{score_info['suit_multiplier']}"
                )
            else:
                self.info_label.setText("1단계: 카드 4장에서 3장 선택")
        else:
            sel = [b for b in self.lower_buttons if b.isChecked()]
            self.confirm_btn.setEnabled(len(self.selected_cards) + len(sel) == 5)
            if len(sel) >= 2:
                combined = self.selected_cards + sel
                score_info = calculate_score(combined, self.selected_joker)
                self.info_label.setText(
                    f"2단계 선택 중 | 족보: {score_info['combo_name']} | 가치합: {score_info['value_sum']} | 배수: x{score_info['suit_multiplier']}"
                )
            else:
                self.info_label.setText("2단계: 아래 카드 4장에서 2장 선택")

    def animate_remove(self, btn):
        # 선택되지 않은 카드 사라지는 애니메이션 효과
        effect = QGraphicsOpacityEffect(btn)
        btn.setGraphicsEffect(effect)

        fade = QPropertyAnimation(effect, b"opacity", self)
        fade.setDuration(600)
        fade.setStartValue(1.0)
        fade.setEndValue(0.0)

        shrink = QPropertyAnimation(btn, b"maximumWidth", self)
        shrink.setDuration(600)
        shrink.setStartValue(btn.width())
        shrink.setEndValue(0)

        fade.start()
        shrink.start()
        QTimer.singleShot(600, lambda: btn.hide())

    def confirm_selection(self):
        # 선택 완료 처리 (1단계 또는 2단계)
        if self.phase == 1:
            selected = [b for b in self.upper_buttons if b.isChecked()]
            if not selected:
                return
            if QMessageBox.question(self, "확정", f"이 {len(selected)}장의 카드를 확정하시겠습니까?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.No:
                return
            self.selected_cards.extend(selected)
            for b in self.upper_buttons:
                if b not in selected:
                    self.animate_remove(b)
                else:
                    b.setEnabled(False)
            self.confirm_btn.setEnabled(False)
            QTimer.singleShot(900, self.start_phase2)
        else:
            selected = [b for b in self.lower_buttons if b.isChecked()]
            if len(self.selected_cards) + len(selected) != 5:
                return

            all_selected = self.selected_cards + selected
            score_info = calculate_score(all_selected, self.selected_joker)

            msg = f"예상 점수: {score_info['total_score']:.2f}점\n"
            msg += f"카드 가치 합: {score_info['value_sum']}점\n"
            msg += f"족보: {score_info['combo_name']} (기본 점수: {score_info['combo_score']})\n"
            msg += f"무늬 배수: x{score_info['suit_multiplier']} ({score_info['top_suit']})\n"
            msg += f"조커: {self.selected_joker if self.selected_joker else '없음'}"

            if QMessageBox.question(self, "카드 조합을 확정 지으시겠습니까?", msg,
                                    QMessageBox.Yes | QMessageBox.No) == QMessageBox.No:
                return

            self.selected_cards.extend(selected)
            for b in self.lower_buttons:
                if b not in selected:
                    self.animate_remove(b)
                else:
                    b.setEnabled(False)
            self.confirm_btn.setEnabled(False)
            QTimer.singleShot(900, self.center_final_cards)

    def start_phase2(self):
        # 2단계 카드 선택 시작
        self.phase = 2
        self.info_label.setText("2단계: 아래 카드 4장에서 2장 선택")
        self.generate_cards(self.lower_layout, self.lower_buttons, 4)

    def center_final_cards(self):
        # 최종 선택된 카드 정중앙 정렬
        for b in self.selected_cards:
            b.setParent(None)
        for layout in (self.upper_layout, self.lower_layout):
            while layout.count():
                layout.takeAt(0)

        center = QHBoxLayout()
        center.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding))
        for b in self.selected_cards:
            center.addWidget(b)
        center.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding))
        self.layout().insertLayout(1, center)

        score_info = calculate_score(self.selected_cards, self.selected_joker)
        self.info_label.setText(
            f"최종 족보: {score_info['combo_name']} | 점수 합: {score_info['value_sum']} | 무늬 배수: x{score_info['suit_multiplier']}"
        )

    def show_joker_cards(self):
        # 조커 카드 선택 창 표시
        dialog = JokerCardDialog(self)
        if dialog.exec_() == QMessageBox.Accepted:
            self.selected_joker = dialog.selected_effect

    def go_back(self):
        # 메인으로 돌아가기 버튼 클릭 시
        if QMessageBox.question(self, "메인 화면으로", "정말 돌아가시겠습니까?",
                                QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.stacked_widget.setCurrentIndex(0)