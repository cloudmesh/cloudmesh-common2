###############################################################
# pytest -v --capture=no tests/test_stopwatch.py
# pytest -v --capture=no tests/test_stopwatch..py::Test_stopwatch.test_001
# pytest -v  tests/test_stopwatch.py
###############################################################


import threading
import time
import unittest
from cloudmesh.common2.stopwatch import StopWatch  # Import your StopWatch class here

stopwatch = StopWatch()


class TestStopWatch(unittest.TestCase):

    def test_single_timer(self):
        stopwatch.start("Timer1")
        time.sleep(1)
        elapsed_time = stopwatch.end("Timer1")
        self.assertAlmostEqual(elapsed_time, 1.0, delta=0.1)

    def test_sequential_timers(self):
        stopwatch.start("Timer2")
        time.sleep(0.5)
        elapsed_time2 = stopwatch.end("Timer2")

        stopwatch.start("Timer3")
        time.sleep(0.5)
        elapsed_time3 = stopwatch.end("Timer3")
        self.assertAlmostEqual(elapsed_time2, 0.5, delta=0.1)
        self.assertAlmostEqual(elapsed_time3, 0.5, delta=0.1)

    def test_non_started_timer(self):
        elapsed_time = stopwatch.end("NonExistentTimer")
        self.assertIsNone(elapsed_time)

    def run_parallel_threads(self):
        num_threads = 5
        threads = []

        def parallel_function():
            current_thread = threading.current_thread()
            name = current_thread.name
            stopwatch.start(name)
            time.sleep(0.5)
            elapsed_time = stopwatch.end(name)
            self.assertAlmostEqual(elapsed_time, 0.5, delta=0.1)

        for _ in range(num_threads):
            thread = threading.Thread(target=parallel_function)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def test_parallel_execution(self):
        self.run_parallel_threads()
        stopwatch.benchmark()  # Print benchmark results

    def test_add_event(self):
        name = "test_timer"
        event_type = "TestEvent"
        event_msg = "This is a test event message"

        stopwatch.start(name, msg="Start of timer")
        stopwatch.add_event(name, event_type, msg=event_msg)
        stopwatch.end(name, msg="End of timer")

        events = stopwatch.events.get(name, [])
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0][0], event_type)
        self.assertEqual(events[0][2], event_msg)

    def test_print_events(self):
        name = "test_timer"
        event_type = "TestEvent"
        event_msg = "This is a test event message"

        stopwatch.start(name, msg="Start of timer")
        stopwatch.add_event(name, event_type, msg=event_msg)
        stopwatch.end(name, msg="End of timer")

        with self.assertLogs(level="INFO") as cm:
            stopwatch.print_events()
            log_output = "\n".join(cm.output)

        self.assertIn(event_type, log_output)
        self.assertIn(event_msg, log_output)

        stopwatch.print_events()

    def test_print_csv(self):
        stopwatch.print_events(tablefmt="csv")
        stopwatch.print_timers(tablefmt="csv")


    # def test_add_and_get_events(self):
    #     thread_name = "TestThread"
    #     event_type = "custom_event"
    #
    #     stopwatch.add_event(thread_name, event_type)
    #     events = stopwatch.get_events(thread_name)
    #
    #     self.assertEqual(len(events), 1)
    #     self.assertEqual(events[0][0], event_type)
    #
    # def test_print_events(self):
    #     thread_name = "TestThread"
    #     event_type = "custom_event"
    #
    #     stopwatch.add_event(thread_name, event_type)
    #
    #     with self.assertLogs(level="INFO") as log_context:
    #         stopwatch.print_events()
    #
    #     expected_log = f"INFO:root:Events for Timer '{thread_name}':\n"\
    #                    f"INFO:root:  {event_type}: {time.time()}"
    #     self.assertIn(expected_log, log_context.output)


if __name__ == "__main__":
    unittest.main()

