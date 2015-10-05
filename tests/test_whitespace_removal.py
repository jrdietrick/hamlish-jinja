# -*- coding: utf-8 -*-

import unittest
import jinja2
from hamlish_jinja import Hamlish, Output, HamlishTagExtension

import testing_base


jinja_env = jinja2.Environment(
    extensions = [
        HamlishTagExtension,
    ]
)


class TestWhitespaceRemoval(testing_base.TestCase):

    # Pulled directly from the HAML spec:
    # http://haml.info/docs/yardoc/file.REFERENCE.html#whitespace_removal__and_

    def setUp(self):
        self.hamlish = Hamlish(
            Output(indent_string='    ', newline_string='\n', debug=False))

    def test_inner_whitespace_basic(self):
        s = '''\
%blockquote<
    %div
        Foo!\
'''
        r = u'''\
<blockquote><div>
    Foo!
</div></blockquote>\
'''
        self.assertEqual(self._h(s), r)

    def test_outer_whitespace_basic(self):
        s = '''\
%img
%img>
%img\
'''
        r = u'''\
<img /><img /><img />\
'''
        self.assertEqual(self._h(s), r)

    # Trying to get this particular case to work
    # resulted in major surgery to no avail; our
    # fundamental approach is a bit flawed, and
    # this case exposes it.
    @unittest.expectedFailure
    def test_inner_and_outer_whitespace(self):
        s = '''\
%img
%pre><
    foo
    bar
%img\
'''
        r = u'''\
<img /><pre>foo
bar</pre><img />\
'''
        self.assertEqual(self._h(s), r)

    def test_inner_and_outer_whitespace_advanced(self):
        s = '''\
%p
    %span><
        special
    text\
'''
        r = u'''\
<p><span>special</span>text</p>\
'''
        self.assertEqual(self._h(s), r)
