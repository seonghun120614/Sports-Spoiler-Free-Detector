from dataclasses import dataclass, field

from feature_extractor.extractor import EntityExtractor

@dataclass
class GlinerExtractor(EntityExtractor):
    labels: list[str] = field(default_factory=list)

    def __post_init__(self):
        print("모델 로딩 중...")
        from gliner2 import GLiNER2
        self._model = GLiNER2.from_pretrained("fastino/gliner2-base-v1")
        print("모델 로딩 완료")

    @property
    def model(self):
        return self._model

    def extract(self, target: str):
        # Debugging Code
        # print(result)
        # {'entities': {'company': ['Apple'], 'person': ['Tim Cook'], 'product': ['iPhone 15'], 'location': ['Cupertino']}}

        return self.model.extract_entities(target, self.labels)

# For test
if __name__ == "__main__":
    extractor = GlinerExtractor(labels = ["win", "defeat", "draw", "score", "goal"])
    print(extractor.extract("game is score 1:2 and winning red team"))