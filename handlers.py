class Handler:
    """
    An object that handles method calls from the Parser.
    The Parser will call the start() and end() methods at the
    beginning of each block, with the proper block name as a
    parameter. The sub() method will be used in regular expression
    substitution. When called with a name such as 'emphasis', it will
    return a proper substitution function.
    """

    def callback(self, prefix, name, *args):
        method = getattr(self, prefix + name, None)
        if callable(method):
            return method(*args)

    def start(self, name):
        self.callback('start_', name)

    def end(self, name):
        self.callback('end_', name)

    def sub(self, name):
        def substitution(match):
            result = self.callback('sub_', name, match)
            if result is None:
                return match.group(0)
            return result

        return substitution


class HTMLRenderer(Handler):
    """
    A specific handler used for rendering HTML.
    The methods in HTMLRenderer are accessed from the superclass
    Handler's start(), end(), and sub() methods. They implement a basic markup
     as used in HTML documents.
    """

    @staticmethod
    def start_document():
        print('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Title</title></head><body>')

    @staticmethod
    def end_document():
        print('print</body></html>')

    @staticmethod
    def start_paragraph():
        print('<p>')

    @staticmethod
    def end_paragraph():
        print('</p>')

    @staticmethod
    def start_heading():
        print('<h2>')

    @staticmethod
    def end_heading():
        print('</h2>')

    @staticmethod
    def start_list():
        print('<ul>')

    @staticmethod
    def end_list():
        print('</ul>')

    @staticmethod
    def start_list_item():
        print('<li>')

    @staticmethod
    def end_list_item():
        print('</li>')

    @staticmethod
    def start_title():
        print('<h1>')

    @staticmethod
    def end_title():
        print('</h1>')

    @staticmethod
    def _format_match_group(pattern, match):
        return pattern.format(match.group(1))

    @classmethod
    def sub_emphasis(cls, match):
        return cls._format_match_group('<em>{}</em>', match)

    @classmethod
    def sub_url(cls, match):
        return cls._format_match_group('<a href={0}>{0}</a>', match)

    @classmethod
    def sub_mail(cls, match):
        return cls._format_match_group('<a href=mailto:{0}>{0}</a>', match)

    @staticmethod
    def feed(data):
        print(data)
