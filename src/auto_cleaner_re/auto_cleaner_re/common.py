from typing import TYPE_CHECKING
from mcdreforged.api.rtext import RTextMCDRTranslation
from mcdreforged.api.types import ServerInterface, PluginServerInterface, Metadata

if TYPE_CHECKING:
    from auto_cleaner_re.config import Configuration
    from auto_cleaner_re.worker import AutoCleanWorker


server_inst: PluginServerInterface = ServerInterface.psi()
metadata: Metadata = server_inst.get_self_metadata()
config: "Configuration"
item_counter: bool = True


def tr(key: str, *args, **kwargs) -> RTextMCDRTranslation:
    return server_inst.rtr("{}.{}".format(metadata.id, key), *args, **kwargs)


def load_common():
    from auto_cleaner_re.config import Configuration
    from auto_cleaner_re.worker import AutoCleanWorker

    global config, worker, item_counter
    config = Configuration.load()
    worker = AutoCleanWorker()
    item_counter = True
