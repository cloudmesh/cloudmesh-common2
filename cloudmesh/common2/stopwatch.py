import threading
import time
from tabulate import tabulate
import logging

class StopWatch:
    def __init__(self, watch="Cloudmesh"):
        self.lock = threading.Lock()
        self.timers = {}
        self.events = {}
        self.watch = watch

        logging.basicConfig(level=logging.INFO,
                            format=f'%(asctime)s - %(levelname)s - ({watch}) - %(message)s')

        logging.info("StopWatch initialized")

    def start(self, name, msg=None):
        with self.lock:
            msg = msg or "start: " + name

            if name not in self.timers:
                self.timers[name] = {
                    "start_time": time.time(),
                    "start_message": msg,
                    "end_message": ""}
                logging.info(f"{self.watch} Timer '{name}' started. {msg}")

    def end(self, name, msg=None):
        with self.lock:
            msg = msg or "end: "+ name

            if name in self.timers:
                timer = self.timers.pop(name)
                elapsed_time = time.time() - timer["start_time"]
                timer["end_message"] = msg
                self.timers[name] = timer
                logging.info("%s Timer '%s' ended. Elapsed time: %.4f seconds. %s", self.watch, name, elapsed_time, msg)
                return elapsed_time
            else:
                logging.warning("%s Timer '%s' was not started", self.watch, name)
                return None

    def add_event(self, name, event_type, msg=""):
        with self.lock:
            if name not in self.events:
                self.events[name] = []
            self.events[name].append((event_type, time.time(), msg))
            logging.info("%s Event added to Timer '%s': %s - %s", self.watch, name, event_type, msg)

    def get_events(self, tablefmt="grid"):
        with self.lock:
            if self.events:
                headers = ["Watch Name",
                           "Timer Name",
                           "Event Type",
                           "Event Time",
                           "Event Message"]
                table_data = []
                for name, events in self.events.items():
                    for event in events:
                        event_type, event_time, event_msg = event
                        event_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(event_time))
                        table_data.append([self.watch, name, event_type, event_time_str, event_msg])

                if tablefmt == "csv":
                    result = []
                    for row in table_data:
                        result.append("#csv "+ ", ".join([str(element) for element in row]))
                    result = "\n".join(result)
                else:
                    result = tabulate(table_data, headers=headers, tablefmt=tablefmt)
                logging.info("\nEvents in Columns:\n%s", result)
                return result
            else:
                logging.info("No events recorded.")

    def print_events(self, tablefmt="grid"):
        r = self.get_events(tablefmt=tablefmt)
        print (r)

    def get_timers(self, tablefmt="grid"):
        with self.lock:
            if self.timers:
                headers = ["Watch Name",
                           "Timer Name",
                           "Start Time",
                           "End Time",
                           "Elapsed Time",
                           "Start Message",
                           "End Message"]
                table_data = []
                for name, timer in self.timers.items():
                    elapsed_time = time.time() - timer["start_time"]
                    start_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timer["start_time"]))
                    end_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timer["start_time"] + elapsed_time))
                    table_data.append([self.watch, name, start_time_str, end_time_str, elapsed_time, timer["start_message"],
                                       timer["end_message"]])
                if tablefmt == "csv":
                    result = []
                    for row in table_data:
                        result.append("#csv "+ ", ".join([str(element) for element in row]))
                    result = "\n".join(result)
                else:
                    result = tabulate(table_data, headers=headers, tablefmt=tablefmt)
                logging.info("\nTimers in Columns:\n%s", result)
                return result
            else:
                logging.info("No timers started.")

    def print_timers(self, tablefmt="grid"):
        r = self.get_timers(tablefmt=tablefmt)
        print (r)

    def benchmark(self):
        self.print_timers()
        self.print_events()


if __name__ == "__main__":
    def example_function(stopwatch):
        name = threading.currentThread().getName()
        stopwatch.start(name)
        time.sleep(1)  # Simulate some work
        elapsed_time = stopwatch.end(name)
        if elapsed_time is not None:
            logging.info("Thread '%s': Elapsed time: %.4f seconds", name, elapsed_time)
        else:
            logging.info("Thread '%s': Timer not started", name)

    stopwatch = StopWatch()

    threads = []
    for i in range(5):
        thread = threading.Thread(target=example_function, args=(stopwatch,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    logging.info("\nBenchmark Results:")
    stopwatch.benchmark()
