import logging
import logging.handlers
import os


class Logger(object):
    """
    logger class encapsulates functionality to create a logger
    that has formatter and handler defined.
    """

    def __init__(self, log_file, log_dir=None):
        self.log_dir = log_dir
        self.log_file = log_file

    def _getLogfile(self):
        if self.log_dir and os.path.exists(self.log_dir):
            logfile = '{0}/{1}'.format(self.log_dir, self.log_file)
        else:
            logfile = self.log_file
        return logfile

    def getLogger(self):
        """
        creates and returns the logger object
        :return:
        """
        l = logging.getLogger(
            name=self.log_file[0:self.log_file.find('.')]
        )
        l.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        # rotating the log files
        handler = logging.handlers.RotatingFileHandler(
            self._getLogfile(),
            maxBytes=5 * 1024 * 1024,
            backupCount=2
        )
        handler.setFormatter(formatter)
        l.addHandler(handler)
        return l
