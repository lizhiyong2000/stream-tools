import base64
import threading
import time
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from playlist.crawler.common.playlist_crawler import PlaylistCrawler
from playlist.downloader.m3u8_downloader import M3u8Downloader
from playlist.indexer.m3u8_indexer import M3u8Indexer
# from playlist.scheduler.crawler_scheduler import CrawlerScheduler


class ThumbWatcher(threading.Thread):

    def __init__(self, thumb_path):
        threading.Thread.__init__(self)
        self.observer = Observer()
        self.thumb_path = thumb_path




    def run(self):
        event_handler = ThumbHandler()
        self.observer.schedule(event_handler, self.thumb_path, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class ThumbHandler(FileSystemEventHandler):

    mongo_url = 'mongodb://192.168.2.26:32717,192.168.2.26:32727,192.168.2.26:32737/playlist?replicaSet=rs0'
    m3u8_indexer = M3u8Indexer(mongo_url, 'playlist', 'm3u8')

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        if event.src_path.endswith(".jpg") and (event.event_type == 'created' or event.event_type == 'modified'):
            # Take any action here when a file is first created.
            print("Received event - %s" % event.src_path)


            file_name = Path(event.src_path).name

            url = bytes.decode(base64.b64decode(file_name[:-4]))

            ThumbHandler.m3u8_indexer.index_thumb(url, file_name)



