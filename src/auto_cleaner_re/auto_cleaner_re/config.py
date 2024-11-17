from mcdreforged.api.types import PluginServerInterface, PermissionLevel
from mcdreforged.api.utils import Serializable

from auto_cleaner_re import common


class Configuration(Serializable):
    enabled: bool = True
    permission: int = PermissionLevel.HELPER
    ignore_player_items: bool = True
    ignore_distance: int = 5
    clean_interval_sec: float = 300

    @staticmethod
    def get_psi() -> PluginServerInterface:
        return common.server_inst

    @classmethod
    def load(cls) -> "Configuration":
        return cls.get_psi().load_config_simple(target_class=cls)

    def save(self):
        self.get_psi().save_config_simple(self)
