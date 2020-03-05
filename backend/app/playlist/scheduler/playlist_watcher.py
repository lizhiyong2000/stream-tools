import threading
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from playlist.crawler.common.playlist_crawler import PlaylistCrawler
from playlist.downloader.m3u8_downloader import M3u8Downloader
from playlist.indexer.m3u8_indexer import M3u8Indexer
# from playlist.scheduler.crawler_scheduler import CrawlerScheduler


class PlaylistWatcher(threading.Thread):
    def __init__(self, playlist_path):
        threading.Thread.__init__(self)
        self.observer = Observer()
        self.playlist_path = playlist_path


    def run(self):
        event_handler = PlaylistHandler()
        self.observer.schedule(event_handler, self.playlist_path, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class PlaylistHandler(FileSystemEventHandler):

    mongo_url = 'mongodb://192.168.2.26:32717,192.168.2.26:32727,192.168.2.26:32737/playlist?replicaSet=rs0'
    m3u8_indexer = M3u8Indexer(mongo_url, 'playlist', 'm3u8')

    thumb_path = None


    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        if event.src_path.endswith("m3u8") and (event.event_type == 'created' or event.event_type == 'modified'):
            # Take any action here when a file is first created.
            print("Received event - %s" % event.src_path)

            PlaylistHandler.m3u8_indexer.index(event.src_path)

            M3u8Downloader(url=event.src_path,
                           download_path=PlaylistHandler.thumb_path).start()


if __name__ == '__main__':
    w = PlaylistWatcher(watch_path=PlaylistCrawler.result_path)
    w.run()
