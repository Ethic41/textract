from fbs_runtime.application_context import ApplicationContext
from ui.textract import TextractGui

import sys


def main():
    appctxt = ApplicationContext()
    window = TextractGui()
    window.show()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
