# utils.py: 점수 계산 및 족보 판별 등 공통 게임 로직 함수들을 정의함.

from collections import Counter

def calculate_score(cards):
    if len(cards) < 1:
        return {
            "combo_name": "-",
            "combo_score": 0,
            "value_sum": 0,
            "suit_multiplier": 1.0,
            "top_suit": "-",
            "total_score": 0
        }

    suit_priority = {'♠': 4, '♦': 3, '♥': 2, '♣': 1}
    suit_multiplier = {'♠': 2.0, '♦': 1.75, '♥': 1.5, '♣': 1.25}
    rank_order = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    rank_value = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
        'J': 15, 'Q': 20, 'K': 25, 'A': 30
    }

    suits, ranks, values = [], [], []
    for btn in cards:
        suit, rank = btn.text().split()
        suits.append(suit)
        ranks.append(rank)
        values.append(rank_value[rank])

    value_sum = sum(values)
    rank_count = Counter(ranks)
    counts = sorted(rank_count.values(), reverse=True)
    is_flush = len(set(suits)) == 1

    rank_indices = sorted([rank_order.index(r) for r in ranks])
    is_straight = len(rank_indices) >= 5 and all(rank_indices[i]+1 == rank_indices[i+1] for i in range(4))
    is_back_straight = sorted(ranks, key=lambda r: rank_order.index(r)) == ['2', '3', '4', '5', 'A']
    is_mountain = sorted(ranks, key=lambda r: rank_order.index(r)) == ['10', 'J', 'Q', 'K', 'A']

    combo = "노 페어"
    base_score = 10

    if is_flush and is_mountain:
        combo = "로열 스트레이트 플러쉬"
        base_score = 100
    elif is_flush and is_back_straight:
        combo = "백 스트레이트 플러쉬"
        base_score = 90
    elif is_flush and is_straight:
        combo = "스트레이트 플러쉬"
        base_score = 80
    elif 4 in counts:
        combo = "포카드"
        base_score = 70
    elif 3 in counts and 2 in counts:
        combo = "풀하우스"
        base_score = 60
    elif is_flush:
        combo = "플러쉬"
        base_score = 50
    elif is_mountain:
        combo = "마운틴"
        base_score = 45
    elif is_back_straight:
        combo = "백스트레이트"
        base_score = 44
    elif is_straight:
        combo = "스트레이트"
        base_score = 40
    elif 3 in counts:
        combo = "트리플"
        base_score = 30
    elif counts.count(2) == 2:
        combo = "투 페어"
        base_score = 25
    elif counts.count(2) == 1:
        combo = "원 페어"
        base_score = 20

    top_suit = max(suits, key=lambda s: suit_priority.get(s, 0))
    multiplier = suit_multiplier.get(top_suit, 1.0)

    if combo == "백스트레이트":
        a_suits = [suits[i] for i, r in enumerate(ranks) if r == 'A']
        if a_suits:
            top_suit = max(a_suits, key=lambda s: suit_priority[s])
            multiplier = suit_multiplier[top_suit]

    total_score = (base_score + value_sum) * multiplier

    return {
        "combo_name": combo,
        "combo_score": base_score,
        "value_sum": value_sum,
        "suit_multiplier": multiplier,
        "top_suit": top_suit,
        "total_score": total_score
    }