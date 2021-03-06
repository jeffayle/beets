"""Some common functionality for beets' test cases."""
import time
import sys

# Mangle the search path to include the beets sources.
sys.path.insert(0, '..')
import beets.library

# Dummy item creation.
def item(): return beets.library.Item({
    'title':            u'the title',
    'artist':           u'the artist',
    'albumartist':      u'the album artist',
    'album':            u'the album',
    'genre':            u'the genre',
    'composer':         u'the composer',
    'grouping':         u'the grouping',
    'year':             1,
    'month':            2,
    'day':              3,
    'track':            4,
    'tracktotal':       5,
    'disc':             6,
    'disctotal':        7,
    'lyrics':           u'the lyrics',
    'comments':         u'the comments',
    'bpm':              8,
    'comp':             True,
    'path':             'somepath',
    'length':           60.0,
    'bitrate':          128000,
    'format':           'FLAC',
    'mb_trackid':       'someID-1',
    'mb_albumid':       'someID-2',
    'mb_artistid':      'someID-3',
    'mb_albumartistid': 'someID-4',
    'album_id':         None,
})


# Mock timing.

class Timecop(object):
    """Mocks the timing system (namely time() and sleep()) for testing.
    Inspired by the Ruby timecop library.
    """
    def __init__(self):
        self.now = time.time()

    def time(self):
        return self.now
    
    def sleep(self, amount):
        self.now += amount

    def install(self):
        self.orig = {
            'time': time.time,
            'sleep': time.sleep,
        }
        time.time = self.time
        time.sleep = self.sleep

    def restore(self):
        time.time = self.orig['time']
        time.sleep = self.orig['sleep']


# Mock I/O.

class InputException(Exception):
    def __init__(self, output=None):
        self.output = output
    def __str__(self):
        msg = "Attempt to read with no input provided."
        if self.output is not None:
            msg += " Output: %s" % repr(self.output)
        return msg
class DummyOut(object):
    encoding = 'utf8'
    def __init__(self):
        self.buf = []
    def write(self, s):
        self.buf.append(s)
    def get(self):
        return ''.join(self.buf)
    def clear(self):
        self.buf = []
class DummyIn(object):
    encoding = 'utf8'
    def __init__(self, out=None):
        self.buf = []
        self.reads = 0
        self.out = out
    def add(self, s):
        self.buf.append(s + '\n')
    def readline(self):
        if not self.buf:
            if self.out:
                raise InputException(self.out.get())
            else:
                raise InputException()
        self.reads += 1
        return self.buf.pop(0)
class DummyIO(object):
    """Mocks input and output streams for testing UI code."""
    def __init__(self):
        self.stdout = DummyOut()
        self.stdin = DummyIn(self.stdout)

    def addinput(self, s):
        self.stdin.add(s)

    def getoutput(self):
        res = self.stdout.get()
        self.stdout.clear()
        return res
    
    def readcount(self):
        return self.stdin.reads

    def install(self):
        sys.stdin = self.stdin
        sys.stdout = self.stdout

    def restore(self):
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__
