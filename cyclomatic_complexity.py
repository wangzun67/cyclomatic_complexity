import os
import argparse
from concurrent.futures import ThreadPoolExecutor

from tree_sitter import Language, Parser

LIB_PATH = "build/my-languages.so"  # 需要替换成对应的路径
LANGUAGES = [
    "tree-sitter-go",
    "tree-sitter-python",
    "tree-sitter-javascript",
]
SUFFIX_2_LANGUAGE = {
    ".go": "go",
    ".py": "python",
    ".js": "javascript",
}

# 控制节点类型
CONTROL_NODE_TYPES = ["if", "for", "while", "case"]


class Util:
    def _check(self, suffix):
        if suffix not in SUFFIX_2_LANGUAGE:
            return False
        return True

    def _load_parser(self, suffix):
        Language.build_library(LIB_PATH, LANGUAGES)
        lang = Language(LIB_PATH, SUFFIX_2_LANGUAGE[suffix])
        parser = Parser()
        parser.set_language(lang)
        return parser

    def _traverse(self, cursor):
        cyclomatic_complexity = 1
        from_parent = False
        while True:
            if not from_parent:
                if cursor.goto_first_child():
                    if cursor.node.type in CONTROL_NODE_TYPES:
                        cyclomatic_complexity += 1
                    continue
            if cursor.goto_next_sibling():
                from_parent = False
                if cursor.node.type in CONTROL_NODE_TYPES:
                    cyclomatic_complexity += 1
                continue
            if cursor.goto_parent():
                from_parent = True
                continue
            break
        return cyclomatic_complexity

    def get_cyclomatic_complexity(self, file_path):
        suffix = os.path.splitext(file_path)[-1]
        if not self._check(suffix):
            print("this language does not support. file_path: %s" % file_path)
            return
        parser = self._load_parser(suffix)
        with open(file_path, "rb") as fd:
            data = fd.read()
        tree = parser.parse(data)
        cursor = tree.walk()
        cyclomatic_complexity = self._traverse(cursor)
        return cyclomatic_complexity


def handle(file_path):
    util = Util()
    cc = util.get_cyclomatic_complexity(file_path)
    if cc:
        print("%s cyclomaticcomplexity: %s" % (file_path, cc))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="accept folder or file")
    parser.add_argument("target", help="target folder or file")
    args = parser.parse_args()
    if os.path.isfile(args.target):
        handle(args.target)
    elif os.path.isdir(args.target):
        max_workers = 3  # 可配置
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for file in os.listdir(args.target):
                executor.submit(handle, os.path.join(args.target, file))
    else:
        print("target folder or file error")
