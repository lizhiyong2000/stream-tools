import os

from playlist.scheduler.playlist_watcher import PlaylistWatcher, PlaylistHandler
from playlist.scheduler.thumb_watcher import ThumbWatcher


class CrawlerScheduler:

    cwd = os.getcwd()

    playlist_download_path = os.path.join(os.getcwd(), "result", "playlist")

    thumb_download_path = os.path.join(os.getcwd(), "result", "thumb")

    playlist_watch = False

    PlaylistHandler.thumb_path = thumb_download_path

    def run(self):

        print("playlist path:" + self.playlist_download_path)
        w = PlaylistWatcher(playlist_path=self.playlist_download_path)
        w.start()

        print("thumb path:" + self.thumb_download_path)

        w = ThumbWatcher(thumb_path=self.thumb_download_path)
        w.start()


