import threading
import time


class TimerThread(threading.Thread):
    def __init__(self, countdown_time, player_name, game_controller):
        super().__init__()
        self.countdown_time = countdown_time
        self.player_name = player_name
        self.game_controller = game_controller
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()
        self.started = False

    def run(self):
        self.started = True
        while not self._stop_event.is_set() and self.countdown_time > 0:
            if not self._pause_event.is_set():
                time.sleep(1)
                self.countdown_time -= 1
                print(f"Remaining time: {self.countdown_time} seconds")
            else:
                while self._pause_event.is_set() and not self._stop_event.is_set():
                    time.sleep(1)
        if self.countdown_time == 0:
            self.game_controller.end_game(self.player_name)

    def stop(self):
        self._stop_event.set()

    def pause(self):
        self._pause_event.set()

    def continue_countdown(self):
        self._pause_event.clear()

    def restart(self):
        self._stop_event.clear()


# Timer logic
# if self.is_white_turn:
#     if self.black_timer.started:
#         self.black_timer.pause()
#     if self.white_timer.started:
#         self.white_timer.restart()
#     else:
#         self.white_timer.start()
# else:
#     if self.white_timer.started:
#         self.white_timer.pause()
#     if self.black_timer.started:
#         self.black_timer.restart()
#     else:
#         self.black_timer.start()
