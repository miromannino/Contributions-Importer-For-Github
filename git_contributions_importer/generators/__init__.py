#!/usr/bin/python3

from .Generator import Generator
from .JsGenerator import JsGenerator
from .JavaGenerator import JavaGenerator
from .CssGenerator import CssGenerator
from .CppGenerator import CppGenerator
from .CGenerator import CGenerator
from .PyGenerator import PyGenerator
from .JsonGenerator import JsonGenerator
from .LuaGenerator import LuaGenerator
from .PhpGenerator import PhpGenerator
from .HtmlGenerator import HtmlGenerator
from .BashGenerator import BashGenerator
from .SqlGenerator import SqlGenerator
from .ScalaGenerator import ScalaGenerator
from .TsGenerator import TsGenerator

available_generators = {
    '.md': Generator,
    '.txt': Generator,
    '.tex': Generator,
    '.js': JsGenerator,
    '.java': JavaGenerator,
    '.css': CssGenerator,
    '.scss': CssGenerator,
    '.cpp': CppGenerator,
    '.c': CGenerator,
    '.py': PyGenerator,
    '.json': JsonGenerator,
    '.lua': LuaGenerator,
    '.php': PhpGenerator,
    '.html': HtmlGenerator,
    '.sh': BashGenerator,
    '.sql': SqlGenerator,
    '.scala': ScalaGenerator,
    '.ts': TsGenerator,
    '.tsx': TsGenerator
}


def apply(content, stats):
    for ext, num in stats.deletions.items():
        if ext in available_generators:
            gen = available_generators[ext]()
            gen.delete(content.get(ext), num)
    for ext, num in stats.insertions.items():
        if ext in available_generators:
            gen = available_generators[ext]()
            gen.insert(content.get(ext), num)
