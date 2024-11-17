from mcdreforged.api.all import (
    PluginServerInterface,
    Literal,
    CommandSource,
    Integer,
    Boolean,
)


from auto_cleaner_re.common import tr, metadata
from auto_cleaner_re import common
from auto_cleaner_re.utils import tag_player_items, cleaned_items

PREFIX = "!!acr"


def show_help(source: CommandSource):
    source.reply(
        tr(
            "help_message",
            name=metadata.name,
            version=metadata.version,
            prefix=PREFIX,
        )
    )


def set_enable(source: CommandSource, value: bool):
    common.config.enabled = value
    common.config.save()
    common.worker.on_config_changed()
    source.reply(tr("set_enable.{}".format(str(value).lower()), value))


def set_interval(source: CommandSource, value: int):
    common.config.clean_interval_sec = value
    common.config.save()
    common.worker.on_config_changed()
    source.reply(tr("set_interval", value))


def set_ignore_distance(source: CommandSource, value: int):
    common.config.ignore_distance = value
    common.config.save()
    common.worker.on_config_changed()
    source.reply(tr("set_ignore_distance", value))


def ignore_player_items(source: CommandSource, value: bool):
    common.config.ignore_player_items = value
    common.config.save()
    common.worker.on_config_changed()
    source.reply(
        tr(
            "ignore_player_items.{}".format(
                str(common.config.ignore_player_items).lower()
            ),
            common.config.ignore_distance,
        )
    )


def register(server: PluginServerInterface):
    server.register_command(
        Literal(PREFIX)
        .requires(
            lambda src: src.has_permission(common.config.permission),
            lambda: tr("permission_denied"),
        )
        .runs(show_help)
        .then(Literal("enable").runs(lambda src: set_enable(src, True)))
        .then(Literal("disable").runs(lambda src: set_enable(src, False)))
        .then(
            Literal("ignore_player_items").then(
                Boolean("true/false").runs(
                    lambda src, ctx: ignore_player_items(src, ctx["true/false"])
                )
            )
        )
        .then(
            Literal("set_interval").then(
                Integer("interval_sec")
                .at_min(45)
                .runs(lambda src, ctx: set_interval(src, ctx["interval_sec"]))
            )
        )
        .then(
            Literal("ignore_distance").then(
                Integer("ignore_distance")
                .at_min(1)
                .runs(lambda src, ctx: set_ignore_distance(src, ctx["ignore_distance"]))
            )
        )
    )
    server.register_help_message(PREFIX, tr("help_message"))

    server.register_event_listener("xevents.player_death", tag_player_items)
    server.register_event_listener("mcdr.general_info", cleaned_items)


def on_load(server: PluginServerInterface, old):
    register(server)
    common.load_common()
    common.worker.on_config_changed()


def on_unload(server: PluginServerInterface):
    common.worker.stop()
    common.worker.join_thread()
