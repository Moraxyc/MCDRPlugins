import threading
import time
import uuid

from typing import Optional
from mcdreforged.api.all import RTextBase,RText,RColor


from auto_cleaner_re import common
from auto_cleaner_re.common import tr, metadata, server_inst
from auto_cleaner_re.utils import clean_items


class AutoCleanWorker:
    def __init__(self):
        self.logger = server_inst.logger
        self.last_clean_time = 0
        self.__thread: Optional[threading.Thread] = None
        self.__stop_event = threading.Event()
        self.__start_stop_lock = threading.Lock()

    def get_next_clean_time(self):
        time_next = self.last_clean_time + common.config.clean_interval_sec
        time_text = time.strftime('%H:%M:%S', time.localtime(time_next))
        return tr('next_clean', round(time_next - time.time(), 1),time_text)


    def on_config_changed(self):
        if common.config.enabled:
            self.start()
        else:
            self.stop()

    def is_running(self):
        return self.__thread is not None and self.__thread.is_alive()

    def start(self):
        with self.__start_stop_lock:
            if not self.is_running():
                self.__stop_event.clear()
                self.__reset_clean_time()
                self.__thread = threading.Thread(
                    name="ACWorker@{}".format(uuid.uuid4().hex[:4]),
                    target=self.__thread_loop,
                )
                self.__thread.start()

    def stop(self):
        self.__stop_event.set()

    def join_thread(self):
        with self.__start_stop_lock:
            thread = self.__thread
        if thread is not None:
            thread.join()

    def __reset_clean_time(self):
        self.last_clean_time = time.time()

    def __thread_loop(self):
        while True:
            next_clean_time = self.last_clean_time + common.config.clean_interval_sec
            time_to_wait = max(0.0, next_clean_time - time.time() - 10.0)
            if self.__stop_event.wait(time_to_wait):
                break
            try:
                server_inst.broadcast(tr("seconds_later", "10"))
                time.sleep(7)
                for i in range(3, 0, -1):
                    server_inst.broadcast(tr("seconds_later", i))
                    time.sleep(1)
                self.clean()
            except Exception:
                self.logger.exception("Error ticking {}".format(metadata.name))
                self.stop()
            finally:
                self.__reset_clean_time()
                server_inst.broadcast(self.get_next_clean_time())

    def clean(self):
        server_inst.broadcast(tr("clean"))
        clean_items(common.config.ignore_player_items)
