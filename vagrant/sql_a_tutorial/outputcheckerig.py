import doctest
from doctest import OutputChecker

FLAG = 'IGNORE_RESULT'
IGNORE_RESULT = doctest.register_optionflag(FLAG)


class OutPutCheckerIR(OutputChecker):

    """
    def __init__(self):
        super(OutPutCheckerIR, self).__init__()
    """

    def check_output(self, want, got, optionflags):
        if optionflags & IGNORE_RESULT:
            return True
        return OutputChecker.check_output(self, want, got, optionflags)

    



