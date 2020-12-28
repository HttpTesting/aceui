import os

__all__ = []

path = os.path.dirname(__file__)
for _, dirs, files in os.walk(path):
    # print(files)
    for file in files:
        if file.endswith(".py") and not file.startswith("__"):
            __all__.append(file.split(".")[0])
            