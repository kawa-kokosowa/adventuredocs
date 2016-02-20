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


class AdventureDoc(object):

    # NOTE: maybe not so much the source_directory, but soup
    def __init__(self, soup):
        self.soup_root = soup

    def __str__(self):

        return self.soup_root.prettify()

    @staticmethod
    def parse_soup(soup):
        """Modifies a BeautifulSoup, to make use of all our
        wonderful features!

        Returns:
            None: This method ONLY modifies the supplied soup.

        """

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

    @staticmethod
    def get_order(directory):
        """
        
        Read the file names in directory/ORDER, which
        will point us to the files we need to read and the
        order in which they're read.

        """

        with open(os.path.join(directory, "ORDER")) as f:
            ordered_section_file_names = [fname.strip() for fname in f.readlines()]

        return ordered_section_file_names

    @classmethod
    def from_directory(cls, directory):
        """Build in order as defined in directory/ORDER

        This is a sloppy method of building the sections, we simply treat
        each section's HTML as strings, finally joining them and making
        tasty soup at the end for you!

        """

        ordered_section_file_names = cls.get_order(directory)
        sections = []

        # we're going to keep track of "progress" per section,
        # which is (basically) a fraction denoting the current
        # index out of the largest index.
        total_section_file_names = len(ordered_section_file_names)

        for file_name_index, file_name in enumerate(ordered_section_file_names):
            # The ORDER file specifies each filename relative to itself, thusly,
            # we must prepend the directory these files are in to read them.
            file_path = os.path.join(directory, file_name)

            with open(file_path) as f:
                file_contents = f.read()

            # Now that we have the file contents, we're going to translate
            # that markdown source into an HTML string, and prepend and
            # append stuff to said string!
            html = markdown.markdown(file_contents)

            section_soup = BeautifulSoup(html, "html.parser")
            cls.parse_soup(section_soup)

            # XXX
            aside = section_soup.new_tag("aside")
            aside['class'] = 'progress'
            aside.string = '%d/%d' % (file_name_index + 1,
                                      total_section_file_names)
            section_soup.append(aside)

            # If there's a next section add the "next section" link!
            try:
                next_file_name = ordered_section_file_names[file_name_index + 1]
                link = section_soup.new_tag("a", href="#" + section_id(next_file_name))
                link["class"] = "next"
                link.string = "Next Section"
                section_soup.append(link)

            except IndexError:
                pass

            section = '<section id="%s">%s</section>' % (section_id(file_name),
                                                         section_soup.prettify())
            sections.append(section)

        # Join the sections together
        sections_string = '\n'.join(sections)

        # Add style for the sections.
        with open("style.css") as f:
            stylesheet_contents = f.read()
            inline_css = "<style>%s</style>" % stylesheet_contents

        html = inline_css + sections_string

        # Make tasty soup, then add some salt to it and serve!
        soup = BeautifulSoup(html, 'html.parser')
        cls.parse_soup(soup)

        return AdventureDoc(soup)


if __name__ == '__main__':
    arguments = docopt.docopt(__doc__)
    source_directory = arguments["<source>"]
    adoc = AdventureDoc.from_directory(source_directory)

    with open(arguments["<destination>"], 'w') as f:
        f.write(str(adoc))
