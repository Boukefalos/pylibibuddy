import os
import glob
import abc

modules = glob.glob(os.path.dirname(__file__) + '/*.py')
__all__ = [os.path.basename(f)[:-3] for f in modules]

class ibuddy:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def test(self):
        return