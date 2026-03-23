from dataclasses import dataclass, field
import torch
from PIL import Image
from accelerate import Accelerator
from feature_extractor.extractor import EntityExtractor

@dataclass
class GroundingDinoDetector(EntityExtractor):
    """
    Grounding DINO 모델을 사용한 Zero-Shot 객체 검출 구현체
    """
    labels: list[str] = field(default_factory=list)
    model_id: str = "IDEA-Research/grounding-dino-tiny"
    threshold: float = 0.25

    def __post_init__(self):
        """초기화 직후 실행: 자원 할당 및 모델 로드"""
        self._device = Accelerator().device
        self._load_model()

    def _load_model(self):
        # Lazy Loading: 메서드 호출 시점에 로드
        from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection
        self._processor = AutoProcessor.from_pretrained(self.model_id)
        self._model = AutoModelForZeroShotObjectDetection.from_pretrained(self.model_id).to(self._device)

    @property
    def prompt_labels(self) -> str:
        """모델 입력용 텍스트 프롬프트 포맷팅"""
        if not self.labels:
            return ""
        return " . ".join(self.labels) + " . "

    def extract(self, path: str) -> list:
        image = Image.open(path).convert("RGB")

        inputs = self._processor(
            images=image,
            text=self.prompt_labels,
            return_tensors="pt"
        ).to(self._device)

        with torch.no_grad():
            outputs = self._model(**inputs)

        results = self._processor.post_process_grounded_object_detection(
            outputs,
            inputs.input_ids,
            threshold=self.threshold,
            text_threshold=self.threshold,
            target_sizes=[image.size[::-1]]
        )[0]

        return self.format_output(results)

    @staticmethod
    def format_output(results: dict) -> list:
        formatted = []
        for score, label, box in zip(results["scores"], results["text_labels"], results["boxes"]):
            formatted.append({
                "label": label,
                "confidence": round(score.item(), 3),
                "box": [round(i, 2) for i in box.tolist()]
            })
        return formatted

# For Test
if __name__ == "__main__":
    extractor = GroundingDinoDetector(labels=["player lifting a trophy"])
    output = extractor.extract("static/example_image.png")
    for result in output:
        print(result)