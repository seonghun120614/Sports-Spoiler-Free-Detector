from dataclasses import dataclass, field
import re
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import patches

def has_score_pattern(text: str) -> int:
    """
    타이틀에서 '2-1', '0:0', '3 0' 같은 점수 패턴을 찾아 Boolean으로 반환합니다.
    """
    if not text:
        return 0

    # 1. 기본 점수 패턴 검색 (1~2자리 숫자 + 구분자 + 1~2자리 숫자)
    # 예: 2-1, 0:0, 4 2, 1 - 0 등
    score_regex = r'\b\d{1,2}\s?[-:\s]\s?\d{1,2}\b'

    matches = re.findall(score_regex, text)

    for match in matches:
        # 공백이나 기호를 제거하고 숫자만 추출 (예: "2 - 1" -> ["2", "1"])
        nums = re.findall(r'\d+', match)

        if len(nums) == 2:
            n1, n2 = int(nums[0]), int(nums[1])

            # 비정상적인 점수 걸러내기
            if n1 < 32 and n2 < 32:
                return 1

    return 0

def has_score_pattern_test():
    # --- 테스트 케이스 ---
    print(has_score_pattern("Man City vs Arsenal 2-1 Highlights"))  # True (2-1)
    print(has_score_pattern("Champions League 0:0 Match Report"))   # True (0:0)
    print(has_score_pattern("Tottenham 3 0 Everton Full Match"))    # True (3 0)
    print(has_score_pattern("Premier League 2025-26 Season"))       # False (연도 필터링)

OUTCOME_DEFINING_TEXT = {
    # 1. Success
    "win", "wins", "victory", "won", "beats", "beat", "triumph", "success", "glory",
    "top", "champions", "kings", "hero", "masterclass",

    # 2. Failure
    "defeat", "defeats", "defeated", "loss", "lose", "lost", "out", "eliminated",
    "relegated", "relegation", "down", "exit", "shock",

    # 3. Draw
    "draw", "draws", "stalemate", "split", "point",

    # 4. Trend
    "unbeaten", "streak", "consecutive", "run", "undefeated",

    # 5. Margin & Type
    "rout", "mauling", "battered", "crushed", "massive", "huge", "thrashing",
    "comeback", "thriller", "dramatic", "last-minute", "epic", "clutch", "secure", "narrow",

    # 6. Tournament Result
    "qualified", "qualification", "through", "advance", "final", "finals",
    "semi-final", "quarter-final", "round-of-16", "ro16", "knockout", "winners", "trophy",
}


def check_spoiler_presence(text: str) -> int:
    """
    텍스트 내에 스포일러 키워드가 포함되어 있으면 1, 없으면 0을 반환합니다.
    """
    if not text:
        return 0

    # 1. 소문자 변환 및 특수문자 제거 (하이픈 '-'은 키워드 매칭을 위해 유지)
    clean_text = re.sub(r'[^a-z0-9\s-]', '', text.lower())

    # 2. 공백 및 하이픈 기준으로 단어 분리하여 세트로 변환
    # (예: 'semi-final' -> {'semi', 'final'} 또는 그대로 'semi-final' 매칭을 위해 전략적 분리)
    words_in_text = set(clean_text.split())

    # 3. 하이픈이 포함된 단어들을 처리하기 위해 원문에서 직접 찾기 로직 병행 (Optional)
    has_spoiler = not words_in_text.isdisjoint(OUTCOME_DEFINING_TEXT)

    # 4. 'semi-final' 같은 합성어 매칭을 위해 추가 체크
    if not has_spoiler:
        for keyword in OUTCOME_DEFINING_TEXT:
            if '-' in keyword and keyword in clean_text:
                has_spoiler = True
                break

    return 1 if has_spoiler else 0

VERB_STRONGLY_PRESENTING_RESULT = {
    # 1. 파괴 및 압살 (Destruction & Crushing)
    "destroyed", "crushed", "smashed", "shattered", "battered", "mauling",
    "demolishing", "breaks", "collapsed", "ripped", "torn",

    # 2. 굴욕 및 압도 (Humiliation & Dominance)
    "humiliation", "humiliating", "outclassed", "silenced", "clinical",
    "masterclass", "dominate", "dominating", "slams", "humbled", "exposed",
    "destroyed", "stunned", "stunner",

    # 3. 비극 및 참사 (Disaster & Heartbreak)
    "heartbreak", "nightmare", "catastrophic", "shock", "shocked", "shocking",
    "disgrace", "shame", "painful", "tragic", "bottled", # 'bottled' 는 리스트에 없으나 축구 맥락상 중요하다고 함 논의

    # 4. 극적 반전 및 기적 (Drama & Miracle)
    "miracle", "epic", "dramatic", "crazy", "insane", "unbelievable",
    "madness", "impossible", "unreal", "clutch", "revenge",

    # 5. 결과 확정 (Sealing the result)
    "sealed", "clinched", "seals", "secured", "confirmed", "finalized"
}

def has_strong_result_word(text: str) -> int:
    """
    텍스트 내에 강력한 결과 표현(VERB_STRONGLY_PRESENTING_RESULT)이 포함되어 있는지 여부를 반환합니다.
    """
    if not text:
        return False

    # 1. 전처리: 소문자 변환 및 특수문자 제거
    clean_text = re.sub(r'[^a-z0-9\s]', '', text.lower())

    # 2. 단어 단위로 분리하여 세트로 변환 (중복 제거 및 검색 속도 향상)
    words_in_text = set(clean_text.split())

    # 3. 세트 교집합 확인: 하나라도 겹치는 단어가 있으면 True 반환
    return 1 if not words_in_text.isdisjoint(VERB_STRONGLY_PRESENTING_RESULT) else 0

SPECIAL_EVENT_KEYWORDS = {
    # 1. 퇴장 (Red Card)
    "red", "card", "redcard", "sent", "off", "dismissed",

    # 2. PK 실축 및 선언 (Penalty Miss & Awarded)
    "penalty", "penalties", "miss", "missed", "misses", "saved",
    "spot", "kick", "var", "controversial", "foul",

    # 3. 자책골 (Own Goal)
    "own", "goal", "og", # 리스트에 'own', 'goal', 'og' 모두 존재 확인

    # 4. 부상 (Injury)
    "injury", "injured", "recovery", "medical", "tear", "painful",

    # 5. 골대 강타 및 결정적 순간 (Woodwork & Crucial Moments)
    "post", "bar", "woodwork", "hit", "missed", "chance", "unlucky", "impossible"
}


def has_special_event(text: str) -> int:
    """
    텍스트 내에 경기 결과에 영향을 주는 특수 사건 키워드가 있는지 확인
    """
    if not text:
        return False

    # 전처리: 소문자화 및 특수문자 제거
    clean_text = re.sub(r'[^a-z0-9\s]', '', text.lower())
    words_in_text = set(clean_text.split())

    # 세트 교집합을 통한 빠른 매칭
    return 1 if not words_in_text.isdisjoint(SPECIAL_EVENT_KEYWORDS) else 0

class DetectionVisualizer:
    """
    객체 검출 결과를 시각화하기 위한 상태 유지형 클래스
    """

    def __init__(self, image_path: str):
        """1. 배경 이미지 로드 및 캔버스 초기화"""
        self.image_path = image_path
        self.image = Image.open(image_path).convert("RGB")

        # Figure와 Axes를 인스턴스 변수로 저장하여 상태를 유지합니다.
        self.fig, self.ax = plt.subplots(1, figsize=(12, 8))
        self.ax.imshow(self.image)

    def draw_box(self,
                 box: list,  # x_min, y_min, x_max, y_max
                 label: str,
                 score: float,
                 color: str = 'lime'):
        """
        2. 유지된 캔버스(Axes) 위에 단일 Bounding Box를 덧그립니다.
        """
        xmin, ymin, xmax, ymax = box
        width = xmax - xmin
        height = ymax - ymin

        # 사각형 패치 추가
        rect = patches.Rectangle(
            (xmin, ymin), width, height,
            linewidth=2, edgecolor=color, facecolor='none'
        )
        self.ax.add_patch(rect)

        # 텍스트 라벨 추가
        self.ax.text(
            xmin, ymin - 5,
            f"{label}: {score:.2f}",
            color='white', fontweight='bold',
            bbox=dict(facecolor=color, alpha=0.5)
        )

    def display(self):
        """3. 최종적으로 완성된 이미지를 화면에 출력합니다."""
        self.ax.axis('off')
        plt.show()

    def draw_line(self):
        self.ax.line


@dataclass
class FeatureConstructor:

    save_path: str = field(default="static/sports_spoiler_detection_features.csv")
    cursor: int = 0

    def write_row(self,
                  trophy: bool,
                  happy: float | bool,
                  sadness: float | bool,
                  angry: float | bool,
                  astonished: float | bool,
                  arms_outstretched: bool,
                  sliding_posture: bool,
                  hug_posture: bool,
                  winning_confidence: float,
                  lose_confidence: float,
                  draw_confidence: float,
                  score: bool):
        # 1. 입력된 파라미터를 딕셔너리로 변환
        new_row = pd.DataFrame([kwargs])

        # 2. 파일 존재 여부 확인 (헤더 추가 결정)
        file_exists = os.path.isfile(self.save_path)

        # 3. 데이터 저장 (mode='a'는 append 모드)
        new_row.to_csv(
            self.save_path,
            mode='a',
            index=False,
            header=not file_exists,
            encoding='utf-8-sig'
        )

        # 커서 업데이트 (필요 시)
        self.cursor += 1

def is_advanced_score(text: str):
    # 특수문자와 영문 구분자를 포괄하는 패턴
    pattern = r"^\d+\s*(?:[-:대/~.,]|vs|to|v)\s*\d+$"
    return bool(re.fullmatch(pattern, text.strip(), re.IGNORECASE))


# For test
if __name__ == "__main__":
    # sample_outputs = [
    #     {"label": "trophy", "confidence": 0.95, "box": [50.0, 50.0, 200.0, 200.0]},
    #     {"label": "person", "confidence": 0.30, "box": [300.0, 150.0, 400.0, 350.0]}
    # ]
    #
    # visualizer = DetectionVisualizer("static/example_image.png")
    #
    # for item in sample_outputs:
    #     if item["confidence"] > 0.5:
    #         visualizer.draw_box(
    #             box=item["box"],
    #             label=item["label"],
    #             score=item["confidence"],
    #         )
    #
    # visualizer.display()
    has_score_pattern_test()