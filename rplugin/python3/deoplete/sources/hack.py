import re
from subprocess import PIPE, Popen

from .base import Base

TOKEN = "AUTO332"
MAX_MENU_WIDTH = 60


class Source(Base):
    def __init__(self, vim):
        Base.__init__(self, vim)
        self.filetypes = ["php", "hack"]
        self.input_pattern = (
            r'\w+|[^. \t]->\w*|\w+::\w*|\w\([\'"][^\)]*|\w\(\w*|\\\w*|\$\w*'
        )
        self.mark = "[Hack]"
        self.name = "hack"
        self.rank = 500
        self.max_menu_width = MAX_MENU_WIDTH

    def on_init(self, context):
        vars = context["vars"]
        self.hh_client = vars.get(
            "deoplete#sources#hack#hh_client", "hh_client"
        )
        self.timeout = vars.get("deoplete#sources#hack#timeout", 0.5)
        self.debug = bool(vars.get("deoplete#sources#hack#debug", 0))

    def get_complete_position(self, context):
        m = re.search(r"[a-zA-Z_0-9\x7f-\xff\\$]*$", context["input"])
        return m.start() if m else -1

    def gather_candidates(self, context):
        [line, column] = self.vim.current.window.cursor
        line -= 1
        lines = self.vim.current.buffer[:]
        lines[line] = lines[line][:column] + TOKEN + lines[line][column:]
        text = "\n".join(lines)
        command = [self.hh_client, "--auto-complete", "--from", "vim"]
        try:
            process = Popen(
                command, stdout=PIPE, stdin=PIPE, universal_newlines=True
            )
            results = process.communicate(input=text)[0].split("\n")[:-1]
            if process.returncode != 0:
                raise Exception(
                    "hh_client returned with: " + str(process.returncode)
                )

            return [parse_result(r) for r in results]
        except Exception as ex:
            if self.debug:
                raise ex
            return []


def parse_result(result):
    word, info = result.split(" ", 1)
    if info.startswith("(function"):
        menu = "func" + info[9:-1]
    else:
        menu = info

    if len(menu) >= MAX_MENU_WIDTH:
        return {"word": word, "menu": menu, "info": info}
    else:
        return {"word": word, "menu": menu}
