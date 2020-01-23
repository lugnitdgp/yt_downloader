#!c:\users\rishab_dugar\documents\github\yt_downloader\myevn\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'pytube','console_scripts','pytube'
__requires__ = 'pytube'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('pytube', 'console_scripts', 'pytube')()
    )
