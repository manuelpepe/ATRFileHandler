import os
import time
import tempfile
import logging

from pathlib import Path
from contextlib import contextmanager
from unittest.mock import MagicMock

from AbsoluteTimedRotatingFileHandler import AbsoluteTimedRotatingFileHandler


@contextmanager
def cdtemp() -> Path:
    """ Temporary changes CWD to a TempDirectory """ 
    orig = os.getcwd()
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            yield Path(tmpdir)
    finally:
        os.chdir(orig)


def test_creates_cache_on_start():
    with cdtemp() as _:
        handler = AbsoluteTimedRotatingFileHandler("test.log", when="S", interval=10, backupCount=3)
        assert handler._cache_filename().exists()


def test_updates_cache_on_rollover():
    with cdtemp() as _:
        # create logger, handler and mock for method that writes cache
        logger = logging.getLogger("test")
        logger.setLevel(logging.INFO)
        handler = AbsoluteTimedRotatingFileHandler("test.log", when="S", interval=1, backupCount=3)
        handler._write_next_rollover_to_cache = MagicMock()
        logger.addHandler(handler)
        # starts in 0 as first call was in __init__ (before mocking)
        assert handler._write_next_rollover_to_cache.call_count == 0
        # should rollover after 1 sec
        time.sleep(1)
        logger.info("test message")
        assert handler._write_next_rollover_to_cache.call_count == 1


def test_reads_from_cache_on_creation():
    with cdtemp() as dirname:
        # fake next rollover
        nextrollover = 123456789
        with open(dirname / "test.log.nextrot", "w") as fp:
            fp.write(str(nextrollover))
        # should be read on creation
        handler = AbsoluteTimedRotatingFileHandler("test.log", when="S", interval=1, backupCount=3)
        assert handler.rolloverAt == nextrollover
