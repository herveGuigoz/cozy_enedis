import json
import os


class FileService:
    @staticmethod
    def read(path: str) -> dict[str, any]:
        # Add .json extension if not present
        if not path.endswith(".json"):
            path += ".json"
        # Add app/etc/ prefix if not present
        if not path.startswith("etc/"):
            path = "etc/" + path
        # Read file
        with open(path, "r") as f:
            return json.load(f)

    @staticmethod
    def write(path: str, content: dict[str, any]) -> None:
        # Add .json extension if not present
        if not path.endswith(".json"):
            path += ".json"
        # Add app/etc/ prefix if not present
        if not path.startswith("etc/"):
            path = "etc/" + path
        # Create directories if they don't exist
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        with open(path, "w") as f:
            json.dump(content, f, indent=2)
