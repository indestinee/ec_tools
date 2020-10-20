from ec_tools.basic_tools.replace_dict import ReplaceDict
from ec_tools import basic_tools


class ColorfulStr:
    def __init__(self):
        self.colors = {
            'black': 30,
            'red': 31,
            'green': 32,
            'yellow': 33,
            'blue': 34,
            'magenta': 35,
            'cyan': 36,
            'white': 37,
            'r': 31,
            'g': 32,
            'y': 33,
            'b': 34,
        }
        self.color_format = '\033[1;{}m'
        self.default = '\033[1;0m'
        table = {
            '(#{})'.format(k): self.color_format.format(v)
            for k, v in self.colors.items()
        }
        table['(#)'] = self.default
        self.replace_colors = ReplaceDict(table)
        self.clean_colors = ReplaceDict({k: '' for k in table.keys()})
        self.done = self('(#g)done(#)')

    def __call__(self, *args) -> str:
        output = basic_tools.touch_suffix(
            ' '.join(map('{}'.format, args)), '(#)')
        output = self.replace_colors.replace(output)
        return output

    def color(self, *args, color='(#g)') -> str:
        return self.replace_colors.replace(color) + self(*args)

    def green(self, *args) -> str:
        return self.color(*args, color='(#g)')

    def red(self, *args) -> str:
        return self.color(*args, color='(#r)')

    def yellow(self, *args) -> str:
        return self.color(*args, color='(#y)')

    def blue(self, *args) -> str:
        return self.color(*args, color='(#b)')

    def clean(self, *args) -> str:
        output = ' '.join(map('{}'.format, args))
        return self.clean_colors.replace(output)


colorful_str = ColorfulStr()
