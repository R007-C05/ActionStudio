# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QWidget
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import Qt, QUrl, QSize
from PySide6.QtGui import QIcon, QPalette, QColor

from ui_video_player import Ui_VideoPlayer
import rc_icons

class VideoPlayer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_VideoPlayer()
        self.ui.setupUi(self)

        self.set_default_screen(self.ui.videoViewport)
        self.set_timestamp_width()

        self.player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.player.setAudioOutput(self.audio_output)

        self.ui.playButton.setIconSize(QSize(16, 16))
        self.icon_play  = QIcon(":/icons/icons/media-playback-start.png")
        self.icon_pause = QIcon(":/icons/icons/media-playback-pause.png")
        self.ui.playButton.setIcon(self.icon_play)

    def set_default_screen(self, viewport):
        palette = viewport.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(Qt.GlobalColor.black))
        viewport.setPalette(palette)
        viewport.setAutoFillBackground(True)

    def seek(self, position_ms):
        self.player.setPosition(position_ms)

    def seek_forward(self):
        self.player.setPosition(min(self.player.position() + 10000, self.player.duration()))

    def seek_backward(self):
        self.player.setPosition(max(self.player.position() - 10000, 0))

    def on_duration_changed(self, duration_ms):
        self.ui.videoSlider.setRange(0, duration_ms)
        self.ui.videoTotalTimeLabel.setText(f"{self._fmt(duration_ms)}")

    def on_position_changed(self, position_ms):
        self.ui.videoSlider.setValue(position_ms)
        self.ui.videoElapsedTimeLabel.setText(f"{self._fmt(position_ms)}")

    def toggle_play(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.ui.playButton.setIcon(self.icon_play)
            self.player.pause()
        else:
            self.player.play()
            self.ui.playButton.setIcon(self.icon_pause)

    def start_playback(self, video_url):
        self.ui.playButton.clicked.connect(self.toggle_play)
        self.ui.seekForwardButton.clicked.connect(self.seek_forward)
        self.ui.seekBackwardButton.clicked.connect(self.seek_backward)
        self.ui.videoSlider.sliderMoved.connect(self.seek)
        self.player.positionChanged.connect(self.on_position_changed)
        self.player.durationChanged.connect(self.on_duration_changed)

        self.ui.playButton.setIcon(self.icon_pause)

        self.player.setVideoOutput(self.ui.videoViewport)
        self.player.setSource(QUrl.fromLocalFile(video_url))
        self.player.play()

    def set_timestamp_width(self):
        font_metrics = self.ui.videoElapsedTimeLabel.fontMetrics()
        fixed_width = font_metrics.horizontalAdvance("00:00:00") + 4  # +8px padding
        self.ui.videoElapsedTimeLabel.setFixedWidth(fixed_width)
        self.ui.videoTotalTimeLabel.setFixedWidth(fixed_width)

        # Right-align elapsed, left-align duration so they hug the slider
        self.ui.videoElapsedTimeLabel.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.ui.videoTotalTimeLabel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

    def _fmt(self, ms):
        s = ms // 1000
        h = s // 3600
        m = (s % 3600) // 60
        s = s % 60
        if self.player.duration() >= 3600000:
            return f"{h:02}:{m:02}:{s:02}"
        return f"{m}:{s:02}"

