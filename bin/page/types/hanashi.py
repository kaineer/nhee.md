import json

from page.types.params import Params


class Hanashi(Params):
    def build_parameters(self):
        raw = self.context.data.get("paragraphs", []) or []
        paragraphs = []
        for item in raw:
            if item is None:
                continue
            text = str(item).strip()
            if text:
                paragraphs.append(text)
        self.params["paragraphs"] = paragraphs
        self.params["vocabulary_json"] = json.dumps(
            self._vocabulary(),
            ensure_ascii=False,
        )

    def _vocabulary(self):
        raw = self.context.data.get("vocabulary", []) or []
        vocabulary = []
        for item in raw:
            if not isinstance(item, dict):
                continue
            vocabulary.append({
                "type": item.get("type") or "",
                "char": item.get("char") or "",
                "reading": item.get("reading") or "",
                "meaning": item.get("meaning") or "",
            })
        return vocabulary
