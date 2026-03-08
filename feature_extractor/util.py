import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import patches

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
                 box: list, # x_min, y_min, x_max, y_max
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



# For test
if __name__ == "__main__":
    sample_outputs = [
        {"label": "trophy", "confidence": 0.95, "box": [50.0, 50.0, 200.0, 200.0]},
        {"label": "person", "confidence": 0.30, "box": [300.0, 150.0, 400.0, 350.0]}
    ]

    visualizer = DetectionVisualizer("static/example_image.png")

    for item in sample_outputs:
        if item["confidence"] > 0.5:
            visualizer.draw_box(
                box=item["box"],
                label=item["label"],
                score=item["confidence"],
            )

    visualizer.display()