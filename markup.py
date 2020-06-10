from handlers import *
from util import *
from rules import *


class Parser:
    """
    A Parser reads a text file, applying rules and controlling a
    handler.
    """

    def __init__(self, handler):
        self.handler = handler
        self.rules = []
        self.filters = []

    def add_rules(self, rule):
        self.rules.append(rule)

    def add_filter(self, pattern, name):
        def filter(block, handler):
            return re.sub(pattern, handler.sub(name), block)

        self.filters.append(filter)

    def parse(self, file):
        self.handler.start('document')
        for block in blocks(file):
            for filter in self.filters:
                block = filter(block, self.handler)
            for rule in self.rules:
                if rule.condition(block):
                    if rule.action(block, self.handler):
                        break
        self.handler.end('document')


class BasicTextParser(Parser):
    """
    A specific Parser that adds rules and filters in its constructor.
    """

    def __init__(self, handler):
        Parser.__init__(self, handler)
        self.add_rules(ListRule())
        self.add_rules(ListItemRule())
        self.add_rules(TitleRule())
        self.add_rules(HeadingRule())
        self.add_rules(ParagraphRule())
        self.add_filter(r'\*(.+?)\*', 'emphasis')
        self.add_filter(r'(http://[\.a-zA-Z/]+)', 'url')
        self.add_filter(r'([\.a-zA-Z]+@[\.a-zA-Z]+[a-zA-Z]+)', 'mail')


handler = HTMLRenderer()
parser = BasicTextParser(handler)
parser.parse(sys.stdin)
