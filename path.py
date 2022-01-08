import os

actual_path = os.path.dirname(os.path.abspath(__file__))
print(actual_path)

templates = os.path.join(actual_path, "gazetteer", "templates")
print(templates)