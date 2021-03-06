#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sublime_plugin


class TaskCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            line_region = self.view.line(region)
            line = self.view.substr(line_region)
            lines = line.split('\n')
            processed_line = '\n'.join([self.process(each_line) for each_line in lines])
            if processed_line != line:
                self.view.replace(edit, line_region, processed_line)

    def process(self, line):
        # below regex looks nice (works in ruby), but it won't work in python:
        # p = re.compile('^(\s*)([-✓])(.*)')
        # http://docs.python.org/howto/unicode
        line = line.encode(self.current_encoding())
        p = re.compile(ur'^(\s*)(-|\xe2\x9c\x93)(.*)', re.UNICODE)
        m = p.match(line)
        if m:
            symbol = '✓' if m.group(2) == '-' else '-'
            result = '%(leading_whitespace)s%(symbol)s%(content)s' % {'leading_whitespace': m.group(1), 'symbol': symbol, 'content': m.group(3)}
            return result.decode(self.current_encoding())
        else:
            return line

    def current_encoding(self):
        if self.view.encoding() == 'Undefined':
            return self.view.settings().get('default_encoding', 'UTF-8')
        else:
            return self.view.encoding()
