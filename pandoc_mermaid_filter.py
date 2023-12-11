#!/usr/bin/env python

import os
import sys
import subprocess

from pandocfilters import toJSONFilter, Para, Image
from pandocfilters import get_filename4code, get_caption, get_extension

# Environment variables with fallback values
MERMAID_BIN = os.path.expanduser(os.environ.get('MERMAID_BIN', 'mmdc'))
RSVG_BIN = os.path.expanduser(os.environ.get('RSVG_BIN', 'rsvg-convert'))
PUPPETEER_CFG = os.environ.get('PUPPETEER_CFG', None)
MERMAID_CFG = os.environ.get('MERMAID_CFG', None)


def mermaid(key, value, format_, _):
    if key == 'CodeBlock':
        [[ident, classes, keyvals], code] = value

        if "mermaid" in classes:
            caption, typef, keyvals = get_caption(keyvals)

            filename = get_filename4code("mermaid", code)
            filetype = get_extension(format_, "pdf")

            src = filename + '.mmd'
            dest = filename + '.' + filetype
            dest2 = filename + '.' + "pdf"

            if not os.path.isfile(dest):
                txt = code.encode(sys.getfilesystemencoding())
                with open(src, "wb") as f:
                    f.write(txt)

                # Default command to execute
                cmd = [MERMAID_BIN, "-f", "-i", src, "-o", dest]

                if MERMAID_CFG is not None:
                    cmd += ["-c", MERMAID_CFG]

                if PUPPETEER_CFG is not None:
                    cmd += ["-p", PUPPETEER_CFG]
                
                sys.stderr.write(f"{cmd} \n")

                subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                sys.stderr.write('Created pdf image ' + dest + '\n')

            return Para([Image([ident, [], keyvals], caption, [dest2, typef])])

def main():
    toJSONFilter(mermaid)


if __name__ == "__main__":
    main()
