class Template:
    def __init__(self, text=""):
        self.text = text

    def apply(self, mappings):
        text = self.text
        for key in mappings:
            value = mappings[key]
            text = text.replace("%" + key + "%", value)
        return Template(text)

    def __str__(self):
        return self.text
