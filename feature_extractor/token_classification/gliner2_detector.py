from feature_extractor.extractor import EntityExtractor

class GlinerExtractor(EntityExtractor):
    def __init__(self, labels: list[str] = None):
        print("모델 로딩 중...")
        from gliner2 import GLiNER2
        self._model = GLiNER2.from_pretrained("fastino/gliner2-base-v1")
        print("모델 로딩 완료")
        if labels is None: labels = ["win", "defeat", "draw", "score", "goal"]
        self._labels = labels

    @property
    def model(self):
        return self._model

    @property
    def labels(self) -> list[str]:
        return self._labels

    @labels.setter
    def labels(self, new_labels: list[str]):
        if not isinstance(new_labels, list):
            raise ValueError("라벨은 반드시 리스트 형태여야 합니다.")
        if len(new_labels) == 0:
            raise ValueError("라벨 리스트가 비어있을 수 없습니다.")
        print(f"로그: 라벨이 {new_labels}로 변경되었습니다.")
        self._labels = new_labels

    def extract(self, target: str):
        # Debugging Code
        # print(result)
        # {'entities': {'company': ['Apple'], 'person': ['Tim Cook'], 'product': ['iPhone 15'], 'location': ['Cupertino']}}

        return self.model.extract_entities(target, self.labels)

if __name__ == "__main__":
    extractor = GlinerExtractor()
    print(extractor.extract("game is score 1:2 and winning red team"))