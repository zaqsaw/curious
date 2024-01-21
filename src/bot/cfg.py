import typing as ty
import yaml
from asyncio import Lock
from asyncio import run
from dataclasses import dataclass
from pathlib import Path

from .logger import get_logger


logger = get_logger()


class Config:
    def __init__(self, config_path):
        with open(config_path / "token.yml", "r") as file:
            self.token = yaml.safe_load(file)["token"]
        with open(config_path / "genz.yml", "r") as file:
            self.genz = yaml.safe_load(file)["quotes"]
        with open(config_path / "ious.yml", "r") as file:
            self.ious = yaml.safe_load(file)["statuses"]
        self.show_file = config_path / "show.yml"
        self.show_map = {}
        self.lock = Lock()
        run(self.load_show_map())

    async def load_show_map(self):
        async with self.lock:
            if not self.show_map and self.show_file.is_file():
                with open(self.show_file, "r") as file:
                    loaded = yaml.safe_load(file)
                if loaded:
                    self.show_map = loaded
            ret = self.show_map
        return ret

    async def save_to_show_map(self, key, value):
        async with self.lock:
            logger.info("saving to %s %s: %s", self.show_file, key, value)
            self.show_map[key] = value
            with open(self.show_file, "w") as file:
                yaml.dump(self.show_map, file)
