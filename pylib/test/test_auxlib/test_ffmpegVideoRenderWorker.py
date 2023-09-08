import contextlib
import pytest
import subprocess
import os

from pylib.auxlib import ffmpegVideoRenderWorker
from pylib.auxlib.ffmpegVideoRenderWorker_ import _check_ffmpeg_installed


def test_check_ffmpeg_installed():
    _check_ffmpeg_installed()


@pytest.mark.heavy
def test_write_frame():
    """Test writing a frame to the ffmpegVideoRenderWorker."""
    outpath = "/tmp/ffmpeg_worker_sample.mp4"
    with contextlib.suppress(FileNotFoundError):
        os.remove(outpath)

    worker = ffmpegVideoRenderWorker(outpath, fps=60.0)
    for i in range(256):
        frame_data = bytes([i] * (1920 * 1080 * 3))
        worker.write_frame(frame_data)

    # Check if the output file is created
    assert os.path.exists(outpath)

    print(f"saved test ffmpegVideoRenderWorker file to {outpath}")


def test_close():
    """Test closing the ffmpegVideoRenderWorker."""
    worker = ffmpegVideoRenderWorker("output.mp4", 30.0)
    worker.close()
    # Asserts that the process has finished
    assert worker._worker_process.poll() is not None


def test_del():
    """Test closing the ffmpegVideoRenderWorker."""
    worker = ffmpegVideoRenderWorker("output.mp4", 30.0)
    worker_process = worker._worker_process
    del worker
    # Asserts that the process has finished
    assert worker_process.poll() is not None
