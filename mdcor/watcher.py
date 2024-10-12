import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from mdcor.converts import convert_to_latex, convert_to_pdf

class MarkdownHandler(FileSystemEventHandler):
    def __init__(self, output_dir='.', convert_pdf=False, template=None):
        self.output_dir = output_dir
        self.convert_pdf = convert_pdf
        self.template = template

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.md'):
            print(f"fichier {os.path.basename(event.src_path)} créé")
            self.process_file(event.src_path)

    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.md'):
            print(f"fichier {os.path.basename(event.src_path)} modifié")
            self.process_file(event.src_path)

    def process_file(self, file_path):
        convert_to_latex(file_path, self.output_dir)
        if self.convert_pdf:
            convert_to_pdf(file_path, self.output_dir, self.template)

def watch_directory(path='.', interval=10, output_dir='.', convert_pdf=False, template=None,convert_bw=False, max_size=None):
    event_handler = MarkdownHandler(output_dir, convert_pdf, template)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(interval)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    watch_directory()