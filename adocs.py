"""AdventureDocs

Choose Your Own Adventure style software
documentation from markdown

Usage:
    adocs <source> <destination>

"""

import os
import docopt
import markdown

from bs4 import BeautifulSoup


def section_id(markdown_file_path):
    """Create a section ID from a path to a markdown file.

    """

    __, section_file_name = os.path.split(markdown_file_path)
    section_id, __ = os.path.splitext(section_file_name)

    return section_id


def parse(string_to_parse):
    html = markdown.markdown(string_to_parse)
    soup = BeautifulSoup(html, "html.parser")

    for ul in soup.find_all("ul"):
        # check if preceeding element is a paragraph
        # with the text content of "CONTEXT_EXAMPLE:"
        # or "NEXT_SECTION:".
        previous_paragraph = ul.find_previous_sibling("p")
        # NOTE: will implement later...
        # if previous_paragraph.text == "CONTEXT_EXAMPLE:":

        if previous_paragraph.text == "NEXT_SECTION:":

            # change each LI into a link
            for li in ul.find_all("li"):
                section_name = section_id(li.string)
                link = soup.new_tag("a", href="#%s" % section_name)
                link.string = section_name
                li.string = ''
                li.append(link)

    return soup.prettify()


def build_sections(directory):
    """Build in order as defined in directory/ORDER

    """

    with open(os.path.join(directory, "ORDER")) as f:
        ordered_section_file_names = [fname.strip() for fname in f.readlines()]

    sections = []

    for file_name_index, file_name in enumerate(ordered_section_file_names):
        file_path = os.path.join(directory, file_name)

        with open(file_path) as f:
            file_contents = parse(f.read())

        try:
            next_file_name = ordered_section_file_names[file_name_index + 1]
            next_section_link = ('<a href="#%s">Next Section</a>' %
                                 section_id(next_file_name))
            file_contents += next_section_link

        except IndexError:
            pass

        section = '<section id="%s">%s</section>' % (section_id(file_name),
                                                     file_contents)
        sections.append(section)

    return '\n'.join(sections)


if __name__ == '__main__':
    arguments = docopt.docopt(__doc__)
    source_directory = arguments["<source>"]

    with open("style.css") as f:
        stylesheet_contents = f.read()
        inline_css = "<style>%s</style>" % stylesheet_contents

    sections = build_sections(source_directory)
    html = inline_css + sections

    with open(arguments["<destination>"], 'w') as f:
        f.write(html)
