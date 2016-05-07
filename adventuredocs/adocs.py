#!/usr/bin/env python
# encoding=utf8

"""AdventureDocs

Choose Your Own Adventure style software
documentation from markdown.

Use markdown files to represent a section of instructions,
and options to skip to a section, or just go to the next
section.

Load a directory of markdown files, which also includes a
file named ORDER which specifies the default order of the
markdown files. The ORDER enables us to have a "next
section" link per section (while you can still present
options to jump to other sections).

Usage:
    adocs <source> [<destination>]

"""

import os
import glob
import docopt
import markdown
import pkgutil
from adventuredocs import plugins

from bs4 import BeautifulSoup


class Section(object):
    """"

    Attributes:
        index (int): --
        name (str): --
        path (str): --
        soup (BeautifulSoup): --

    """

    def __init__(self, index, name, path, soup):
        self.index = index
        self.name = name
        self.path = path
        self.soup = soup

    @classmethod
    def from_file(cls, section_index, path_to_markdown_file):
        """Create a section object by reading
        in a markdown file from path!

        Arguments:
            section_index (int):
            path_to_markdown_file (str): --

        Returns:
            Section

        """

        with open(path_to_markdown_file) as f:
            file_contents = unicode(f.read(), 'utf-8')

        html = markdown.markdown(file_contents)
        section_soup = BeautifulSoup(html, "html.parser")

        # get the file name without the extension
        __, section_file_name = os.path.split(path_to_markdown_file)
        section_name, __ = os.path.splitext(section_file_name)

        return cls(index=section_index,
                   path=path_to_markdown_file,
                   soup=section_soup,
                   name=section_name)


class AdventureDoc(object):
    """A directory of markdown files, with an ORDER file.

    Constants:
        STYLESHEET (str): Stylesheet file relative to
            current directory. The stylesheet's contents
            are prepended to the end-result HTML.
        SECTION_CHOICE_KEYWORD (str): Triggers a proceeding
            list to be a list of links to other sections.
        HIGHLIGHTJS_CSS (str): Hosted HighlightJS CSS/stylesheet
            URI. See: highlightjs.org.
        HIGHLIGHTJS_JS (str): Hosted HighlightJS JavaScript
            URI. See: highlightjs.org.

    """

    STYLESHEET = pkgutil.get_data("adventuredocs", "style.css")
    SECTION_CHOICE_KEYWORD = "NEXT_SECTION:"
    HIGHLIGHTJS_CSS = ("http://cdnjs.cloudflare.com/ajax/libs/highlight.js/"
                       "9.2.0/styles/default.min.css")
    HIGHLIGHTJS_JS = ("http://cdnjs.cloudflare.com/ajax/libs/highlight.js/"
                      "9.2.0/highlight.min.js")

    def __init__(self, sections):
        self.sections = sections

    def build(self):
        all_sections_wrapper = BeautifulSoup('', 'html.parser')

        for section_soup in self.sections:
            section_soup = self.use_plugins_and_wrap(section_soup)
            all_sections_wrapper.append(section_soup)

        self.add_theme_to_soup(all_sections_wrapper)

        return all_sections_wrapper.prettify().encode("UTF-8")

    @staticmethod
    def get_sections(directory):
        """Collect the files specified in the
        ORDER file, returning a list of
        dictionary representations of each file.

        Returns:
            list[Section]: list of sections which

        """

        with open(os.path.join(directory, "ORDER")) as f:
            order_file_lines = f.readlines()

        ordered_section_file_paths = []

        for line_from_order_file in order_file_lines:
            section_path = os.path.join(directory, line_from_order_file)
            ordered_section_file_paths.append(section_path.strip())

        sections = []

        for i, section_file_path in enumerate(ordered_section_file_paths):
            sections.append(Section.from_file(i, section_file_path))

        return sections

    # NOTE: this currently actually changes the section's
    # beautiful soup but should make copy instead!
    def use_plugins_and_wrap(self, section):

        for _, module_name, _ in pkgutil.iter_modules(plugins.__path__):
            module_name = "adventuredocs.plugins." + module_name
            plugin = __import__(module_name, fromlist=["change_soup"])
            change_soup_function = getattr(plugin, "change_soup")
            plugin.change_soup(self, section)

        # limitation of bs4
        section_wrapper = section.soup.new_tag("section")
        section_wrapper["id"] = section.name

        section_wrapper.append(section.soup)

        return section_wrapper

    @classmethod
    def add_theme_to_soup(cls, soup):
        """Let's present our soup nicely!
        
        Prepend <style> element whose contents
        is from the STYLESHEET file. Also add
        the code necessary for syntax highlighting.

        Does not return anything; this modifies
        the supplies soup.

        Arguments:
            soup (BeautifulSoup): The soup to add
                style to.

        Raises:
            IOError: if cls.STYLESHEET not found!

        """

        stylesheet_contents = cls.STYLESHEET

        # Add our custom stylesheet
        style = soup.new_tag('style')
        style.string = stylesheet_contents
        soup.insert(0, style)

        # Add the HighlightJS StyleSheet
        highlightjs_css = soup.new_tag('link')
        highlightjs_css["rel"] = 'stylesheet'
        highlightjs_css['href'] = cls.HIGHLIGHTJS_CSS
        soup.insert(0, highlightjs_css)

        # Add the HighlightJS JavaScript
        highlightjs_js = soup.new_tag('script')
        highlightjs_js["src"] = cls.HIGHLIGHTJS_JS
        soup.insert(0, highlightjs_js)

        # Add the execute script/init for HighlightJS
        init_script = soup.new_tag('script')
        init_script.string = 'hljs.initHighlightingOnLoad();'
        soup.append(init_script)

    @classmethod
    def from_directory(cls, directory):
        ordered_sections = cls.get_sections(directory)

        return AdventureDoc(ordered_sections)


def main():
    arguments = docopt.docopt(__doc__)
    source_directory = arguments["<source>"]
    adoc = AdventureDoc.from_directory(source_directory)

    destination = arguments["<destination>"] or "adocs-output.html"

    with open(destination, 'wb') as f:
        f.write(adoc.build())
