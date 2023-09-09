import contextlib
import os
import subprocess
import typing


def _check_ffmpeg_installed() -> None:
    """Raise if ffmpeg is not installed."""
    try:
        subprocess.check_output(["ffmpeg", "-version"])
    except Exception as e:
        print("ffmpeg installation check failed, is ffmpeg installed?")
        raise e


# adapted from https://www.loekvandenouweland.com/content/render-pyglet-to-mp4-with-python-and-ffmpeg.html
class ffmpegVideoRenderWorker:
    """Initializes an ffmpeg background process to accept raw video frames
    for on-the-fly video rendering to specified output path.

    On deletion or explicit closure, the ffmpeg process is terminated.
    """

    _worker_process: subprocess.Popen

    def __init__(
        self: "ffmpegVideoRenderWorker",
        output_path: str,
        fps: float,
        *,
        frame_width: int = 1920,
        frame_height: int = 1080,
    ) -> None:
        """Initialize worker.

        Parameters
        ----------
        output_path : str
            Path for the output video, must have .mp4 extension.
        fps : float
            Frames per second.
        frame_width : int, default 1920
            Video frame pixel width.
        frame_height : int, default 1080
            Video frame pixel height.
        """
        if not output_path.endswith(".mp4"):
            raise ValueError("{output_path=} must have .mp4 extension")
        # ensure no pre-existing file deceviengly persists in case of failure
        with contextlib.suppress(FileNotFoundError):
            os.remove(output_path)

        _check_ffmpeg_installed()

        frame_size = f"{frame_width}x{frame_height}"
        # fmt: off
        command = [
            "ffmpeg",  # ffmpeg executable
            "-y",  # overwrite output files
            "-f", "rawvideo",  # force format
            "-s", frame_size,  # frame size
            "-pix_fmt", "rgba",  # pixel format
            "-r", str(fps),  # frame rate
            "-i", "-",  # input is pipe
            "-an",  # disable audio
            "-vf", "vflip",  # video filters, vertical flip
            "-vcodec", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "ultrafast",  # https://superuser.com/a/490691
            str(output_path),  # output file
        ]
        # fmt: on
        self._worker_process = subprocess.Popen(command, stdin=subprocess.PIPE)

    def __del__(self: "ffmpegVideoRenderWorker") -> None:
        """Cleanup on destruction, closes worker process."""
        self.close()

    def write_frame(
        self: "ffmpegVideoRenderWorker",
        data: typing.Union[bytes, bytearray],
    ) -> None:
        """Write a frame to the video.

        Parameters
        ----------
        data : Union[bytes, bytearray]
            Bytes of the frame.
        """
        self._worker_process.stdin.write(data)

    def close(self: "ffmpegVideoRenderWorker") -> None:
        """Close the worker process."""
        with contextlib.suppress(Exception):
            self._worker_process.stdin.close()
            self._worker_process.wait()
            self._worker_process.terminate()
