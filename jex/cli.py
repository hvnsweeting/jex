import argparse
import json
import tempfile
import os
import sys
import subprocess
import webbrowser

HTML = """
<html lang="en">
  <head>
    <meta charset="utf-8">
  </head>
  <body style="background: gray; color: white">
    <h1><a href="file://JSONPATH">View file</a></h1>
    <h1>Open web console and access `data` to continue</h1>
    <div id="app"></div>
    <script>
    var app = document.getElementById("app");
    var data = __JSONDATA__;
    app.innerHTML = JSON.stringify(data);
    </script>
  </body>
</html>
"""


def is_json(text):
    try:
        json.loads(text)
        return True
    except Exception:
        return False


def process():
    _, fn = tempfile.mkstemp()
    json_path = fn + ".json"
    with open(fn, "wt") as f, open(json_path, "wt") as jsonf:
        data = sys.stdin.read()
        if is_json(data):
            jsonf.write(data)
            f.write(
                HTML.replace("JSONPATH", json_path).replace(
                    "__JSONDATA__", data
                )
            )
        else:
            # try yaml
            import yaml

            try:
                data = json.dumps(yaml.safe_load(data))
            except Exception as e:
                print("Not a JSON/YAML file, got error", e)
                print("See content at ", json_path)
                jsonf.write(data)
                exit(1)

            jsonf.write(data)
            f.write(
                HTML.replace("JSONPATH", json_path).replace(
                    "__JSONDATA__", data
                )
            )
    print("Wrote", fn)
    return fn


PYTHON_PRELOAD = """
from pprint import pprint
from itertools import *
from functools import *
from operator import *

import json
data = json.load(open("JSONPATH"))
print("{0} {1} {0}".format("=" * 10, "WELCOME TO JEX"))
print("Access the data via name data")
if isinstance(data, list):
    if not data:
        print("Empty list")
    else:
        print("data is a list, with length {}, first elem of type {}".format(len(data), type(data[0])))
elif isinstance(data, dict):
    print("data is a dict, with keys: {}".format(list(data.keys())))
"""


HYLANG_PRELOAD = """
(import json)
(setv data (json.load (open "JSONPATH")))
(print (.format "{0} {1} {0}" (* "=" 10) "WELCOME TO JEX"))
(print "Access the data via name data")

(if (isinstance data list)
  (do
  (if-not data
    (print "Empty list")
    (print (.format "data is a list, with length {}, first elem of type {}" (len data) (type (first data)))))))
"""

OSX_INVOKER = """
#!/bin/sh
exec PYTHON_INTERPRETER -i /tmp/jbox.py
"""


def open_in_webbrowser(fn):
    try:
        # try with option to open dev console
        subprocess.run(["firefox", "--devtools", "file://" + fn])
    except Exception:
        webbrowser.open_new_tab(fn)


RUBY_PRELOAD = """
require 'json'
$data = JSON.parse(File.open('JSONPATH', 'r').read())
puts("data of type %s, access via variable $data" % [$data.class])
"""


NODE_PRELOAD = """
console.log("Using nodejs version: ", process.version);
global.data = require("JSONPATH");
console.log("Access via variable `data`, type: ", typeof(global.data));
if (global.data instanceof Array) {
  console.log("Length: ", global.data.length);
}
"""


def main():
    argp = argparse.ArgumentParser()
    argp.add_argument(
        "-w",
        "--webbrowser",
        action="store_true",
        help="View data using browser feature, access via JS console",
    )
    argp.add_argument(
        "--repl",
        help="TODO, would need preconvert data to each lang",
        choices=["hy", "rb", "node", "js"],
    )
    args = argp.parse_args()
    if args.webbrowser:
        fn = process()
        open_in_webbrowser(fn)
        exit()

    fn = process()
    if args.repl == "hy":
        with open("/tmp/jbox.hy", "wt") as f:
            f.write(HYLANG_PRELOAD.replace("JSONPATH", fn + ".json"))
        cmd = ["hy", "-i", "/tmp/jbox.hy"]
    elif args.repl == "rb":
        with open("/tmp/jbox.rb", "wt") as f:
            f.write(RUBY_PRELOAD.replace("JSONPATH", fn + ".json"))
        cmd = ["irb", "-r", "/tmp/jbox.rb"]
    elif args.repl in {"node", "js"}:
        with open("/tmp/jbox.js", "wt") as f:
            f.write(NODE_PRELOAD.replace("JSONPATH", fn + ".json"))
        cmd = ["node", "-r", "/tmp/jbox.js"]

    else:
        with open("/tmp/jbox.py", "wt") as f:
            f.write(PYTHON_PRELOAD.replace("JSONPATH", fn + ".json"))

        cmd = [
            sys.executable,
            "-i",
            "/tmp/jbox.py",
        ]

    # TODO detect terminal in use
    # TODO run as shell exec instead of subprocess
    cmd = ["gnome-terminal", "--"] + cmd

    if sys.platform == "darwin":
        with open("/tmp/jbox.sh", "wt") as f:
            f.write(OSX_INVOKER.replace("PYTHON_INTERPRETER", sys.executable))
        os.chmod("/tmp/jbox.sh", 0o755)
        try:
            cmd = ["open", "--new", "-a", "iterm", "/tmp/jbox.sh"]
            subprocess.call(cmd)
            exit()
        except Exception:
            cmd = ["open", "--new", "-a", "Terminal", "/tmp/jbox.sh"]

    try:
        subprocess.call(cmd)
    except Exception as e:
        print("Cannot open terminal: {}, Error: {}".format(cmd, e))
        print("fall-back to webbrowser.")
        open_in_webbrowser(fn)


if __name__ == "__main__":
    main()
