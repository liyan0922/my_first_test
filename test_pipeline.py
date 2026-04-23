import time
import subprocess
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class TestRunner(FileSystemEventHandler):
    def __init__(self, test_dir='tests'):
        self.test_dir = test_dir
        self.last_run_time = 0
        self.debounce_seconds = 2
    
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.py'):
            current_time = time.time()
            if current_time - self.last_run_time > self.debounce_seconds:
                self.last_run_time = current_time
                print(f"\n{'='*60}")
                print(f"File changed: {event.src_path}")
                print(f"Running tests...")
                print(f"{'='*60}")
                self.run_tests()
    
    def run_tests(self):
        cmd = [
            'pytest',
            self.test_dir,
            '-v',
            '--html=reports/report.html',
            '--self-contained-html',
            '--cov=pages',
            '--cov-report=html:reports/coverage',
            '--cov-report=term-missing',
            '--headless',
            '--maxfail=1000'
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
            print(result.stdout)
            if result.stderr:
                print("Errors:")
                print(result.stderr)
            print(f"\n{'='*60}")
            print(f"Tests completed with exit code: {result.returncode}")
            print(f"Report generated: reports/report.html")
            print(f"{'='*60}\n")
        except Exception as e:
            print(f"Error running tests: {e}")


def main():
    print("="*60)
    print("Starting test pipeline...")
    print("Watching for file changes...")
    print("Press Ctrl+C to stop")
    print("="*60)
    
    event_handler = TestRunner()
    observer = Observer()
    
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nPipeline stopped.")
    observer.join()


if __name__ == "__main__":
    main()