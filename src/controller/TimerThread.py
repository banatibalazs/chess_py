import threading
import time


class TimerThread(threading.Thread):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            try:
                if not self._pause_event.is_set() and self.game._current_player.time > 0:
                    time.sleep(1)
                    self.game._current_player.time -= 1
                    self.game._gui_controller.update_timer_label(self.game._current_player.time,
                                                                 self.game._current_player.color)
                else:
                    time.sleep(1)
                if self.game._current_player.time == 0:
                    # self.game_controller.end_game(current_player)
                    pass

            except Exception as e:
                print(e)
                self.stop()

    def stop(self):
        self._stop_event.set()

    def pause(self):
        self._pause_event.set()

    def continue_countdown(self):
        self._pause_event.clear()

    def restart(self):
        self._stop_event.clear()
