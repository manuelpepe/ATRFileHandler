# ATRFileHandler

ATRFileHandler, or AbsoluteTimedRotatingFileHandler, is a file handler like [TimedRotatingFileHandler](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.TimedRotatingFileHandler) that caches rollover time for your logfiles across executions, allowing future instances of your application to rotate the logfile in schedule, avoiding surprices of large logfiles that haven't rotated as you expected.

## Diferences with TimedRotatingFileHandler

Python's built-in [`logging.TimedRotatingFileHanndler`](https://docs.python.org/3/library/logging.handlers.html#timedrotatingfilehandler) calculates the initial rollover time at instantiation, meaning that it's lost when the program exits. `ATRFileHandler` catches the next rollover time in a file on the same parent directory as your log files, and loads it at instantiation.

## Install

With pip:

```
pip install ATRFileHandler
```

## Usage

It can be used exactly as the [TimedRotatingFileHandler](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.TimedRotatingFileHandler) from the builting `logging` module.

Example:

```python
import logging
from ATRFileHandler import ATRFileHandler

logger = logging.getLogger()
handler = ATRFileHandler("test.log", when="D", interval=3, backupCount=3)
logger.addHandler(handler)
logger.error("too much rythm")
```

## Running tests

```
pip install -e .
pytest --cov=ATRFileHandler/
```
