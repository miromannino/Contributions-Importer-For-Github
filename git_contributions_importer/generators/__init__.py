#!/usr/bin/python3

from .Generator import Generator
from .JsGenerator import JsGenerator
from .JavaGenerator import JavaGenerator
from .CssGenerator import CssGenerator
from .CppGenerator import CppGenerator
from .CGenerator import CGenerator
from .PyGenerator import PyGenerator
from .RubyGenerator import RubyGenerator
from .JsonGenerator import JsonGenerator
from .KotlinGenerator import KotlinGenerator
from .LuaGenerator import LuaGenerator
from .PhpGenerator import PhpGenerator
from .HtmlGenerator import HtmlGenerator
from .BashGenerator import BashGenerator
from .SqlGenerator import SqlGenerator
from .ScalaGenerator import ScalaGenerator
from .SwiftGenerator import SwiftGenerator
from .TerraformGenerator import TerraformGenerator
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
    '.kt': KotlinGenerator,
    '.lua': LuaGenerator,
    '.php': PhpGenerator,
    '.html': HtmlGenerator,
    '.sh': BashGenerator,
    '.sql': SqlGenerator,
    '.scala': ScalaGenerator,
    '.swift': SwiftGenerator,
    '.ts': TsGenerator,
    '.tsx': TsGenerator,
    '.rb': RubyGenerator
    '.tf': TerraformGenerator
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
