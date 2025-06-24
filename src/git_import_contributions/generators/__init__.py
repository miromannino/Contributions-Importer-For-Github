from .BashGenerator import BashGenerator
from .CGenerator import CGenerator
from .CppGenerator import CppGenerator
from .CsharpGenerator import CsharpGenerator
from .CssGenerator import CssGenerator
from .DartGenerator import DartGenerator
from .Generator import Generator
from .HtmlGenerator import HtmlGenerator
from .JavaGenerator import JavaGenerator
from .JsGenerator import JsGenerator
from .JsonGenerator import JsonGenerator
from .KotlinGenerator import KotlinGenerator
from .LuaGenerator import LuaGenerator
from .PhpGenerator import PhpGenerator
from .PyGenerator import PyGenerator
from .RubyGenerator import RubyGenerator
from .ScalaGenerator import ScalaGenerator
from .SqlGenerator import SqlGenerator
from .SwiftGenerator import SwiftGenerator
from .TerraformGenerator import TerraformGenerator
from .TsGenerator import TsGenerator
from .XamlGenerator import XamlGenerator

available_generators = {
    ".md": Generator,
    ".txt": Generator,
    ".tex": Generator,
    ".js": JsGenerator,
    ".java": JavaGenerator,
    ".css": CssGenerator,
    ".scss": CssGenerator,
    ".cpp": CppGenerator,
    ".c": CGenerator,
    ".cs": CsharpGenerator,
    ".dart": DartGenerator,
    ".py": PyGenerator,
    ".json": JsonGenerator,
    ".kt": KotlinGenerator,
    ".lua": LuaGenerator,
    ".php": PhpGenerator,
    ".html": HtmlGenerator,
    ".sh": BashGenerator,
    ".sql": SqlGenerator,
    ".scala": ScalaGenerator,
    ".swift": SwiftGenerator,
    ".ts": TsGenerator,
    ".tsx": TsGenerator,
    ".rb": RubyGenerator,
    ".tf": TerraformGenerator,
    ".xaml": XamlGenerator,
}


def apply_generator(content, stats):
    for ext, num in stats.deletions.items():
        if ext in available_generators:
            gen = available_generators[ext]()
            gen.delete(content.get(ext), num)
    for ext, num in stats.insertions.items():
        if ext in available_generators:
            gen = available_generators[ext]()
            gen.insert(content.get(ext), num)
