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
    adocs <source> <destination>

"""

import os
import docopt
import markdown

from bs4 import BeautifulSoup


def section_id(markdown_file_path):
    """Create a section ID from a path to a markdown file.

    Currently not very smart; don't expect it to sanitize
    the ID or anything like that. This simply gets the
    filename portion (without extension), but there's room
    for expansion.

    Arguments:
        markdown_file_path (str): Path to a markdown file, it
            may be relative or absolute.

    Returns:
        str: A valid HTML ID for this section.

    Example:
        >>> section_id('some/path/to/source/eaten-by-a-grue.md')
        'eaten-by-a-grue'

    """

    __, section_file_name = os.path.split(markdown_file_path)
    section_id, __ = os.path.splitext(section_file_name)

    return section_id


class AdventureDoc(object):
    """A directory of markdown files, with an ORDER file.

    Constants:
        STYLESHEET (str): Stylesheet file relative to
            current directory. The stylesheet's contents
            are prepended to the end-result HTML.
        SECTION_CHOICE_KEYWORD (str): Triggers a proceeding
            list to be a list of links to other sections.

    """

    STYLESHEET = "style.css"
    SECTION_CHOICE_KEYWORD = "NEXT_SECTION:"

    def __init__(self, soup):
        self.soup = soup

    def __str__(self):

        return self.soup.prettify()

    @classmethod
    def add_special_seasoning(cls, soup):
        """Add our special brand seasoning to the soup!
        
        Modifies a BeautifulSoup, to make use of all our
        wonderful features! This does not return anything,
        it simply modifies a supplied BeautifulSoup.

        Arguments:
            soup (BeautifulSoup): The soup to season!

        Returns:
            None: This method ONLY modifies the supplied soup.

        """

        for ul in soup.find_all("ul"):
            # check if preceeding element is a paragraph
            # whose text is the section choice keyword!
            previous_paragraph = ul.find_previous_sibling("p")

            # NOTE: will implement later...
            # if previous_paragraph.text == "CONTEXT_EXAMPLE:":
            # ... Which will be the toggle blocks. Though, this
            # featuer may be replaced by simply having a way
            # to set a global variable and render content based
            # on what the user set said variable to, e.g.,
            # platform is osx.

            if previous_paragraph.text == cls.SECTION_CHOICE_KEYWORD:

                # We're going to make each LI's contents a link
                # to the markdown file it specifies!
                for li in ul.find_all("li"):
                    section_name = section_id(li.string)
                    link = soup.new_tag("a", href="#%s" % section_name)
                    link.string = section_name
                    li.string = ''
                    li.append(link)

    @staticmethod
    def get_order(directory):
        """Collect the order of sections from directory/ORDER.
        
        Read the file names in directory/ORDER, which
        will point us to the files we need to read and the
        order in which they're read.

        Arguments:
            directory (str): --

        Return:
            list: The sections which compose the AdventureDoc,
                in the correct order.

        """

        with open(os.path.join(directory, "ORDER")) as f:
            ordered_section_file_names = [fname.strip() for fname in f.readlines()]

        return ordered_section_file_names

    @classmethod
    def put_in_nice_bowl(cls, soup):
        """Let's present our soup nicely!
        
        Prepend <style> element whose contents
        is from the STYLESHEET file.

        Does not return anything; this modifies
        the supplies soup.

        Arguments:
            soup (BeautifulSoup): The soup to add
                style to.

        Raises:
            IOError: if cls.STYLESHEET not found!

        """

        with open(cls.STYLESHEET) as f:
            stylesheet_contents = f.read()

        style = soup.new_tag('style')
        style.string = stylesheet_contents
        soup.insert(0, style)

    @classmethod
    def build_section(cls, file_contents, file_name,
                      ordered_section_file_names):

        """Create the HTML for the provided file contents!

        Arguments:
            file_contents (str):
            file_name (str):
            ordered_section_file_names (list[str]):

        Returns:
            BeautifulSoup: --

        """

        total_section_file_names = len(ordered_section_file_names)
        file_name_index = ordered_section_file_names.index(file_name)

        # Transform our markdown file contents into soup which
        # has been graced by our special seasoning!
        html = markdown.markdown(file_contents)
        section_soup = BeautifulSoup(html, "html.parser")
        cls.add_special_seasoning(section_soup)

        # Section Progress/Position
        aside = section_soup.new_tag("aside")
        aside['class'] = 'progress'
        aside.string = '%d/%d' % (file_name_index + 1,
                                  total_section_file_names)
        section_soup.append(aside)

        # If there's a next section add the "next section" link!
        try:
            next_file_name = ordered_section_file_names[file_name_index + 1]
            section_name = section_id(next_file_name)
            link = section_soup.new_tag("a", href="#" + section_name)
            link["class"] = "next"
            link.string = "Next Section"
            section_soup.append(link)

        except IndexError:
            pass

        section_wrapper = section_soup.new_tag("section")
        section_wrapper["id"] = section_id(file_name)

        section_wrapper.append(section_soup)

        return section_wrapper

    @classmethod
    def from_directory(cls, directory):
        """Build an AdventureDoc by processing a directory.

        Arguments:
            directory (str): Path to the directory containing
                the ORDER file along with the sections as
                markdown files.

        Returns:
            AdventureDoc:

        """

        ordered_section_file_names = cls.get_order(directory)
        all_sections_soup = BeautifulSoup('', 'html.parser')

        for file_name in ordered_section_file_names:
            # The ORDER file specifies each filename relative to itself, thusly,
            # we must prepend the directory these files are in to read them.
            file_path = os.path.join(directory, file_name)

            with open(file_path) as f:
                file_contents = f.read()

            section_soup = cls.build_section(file_contents, file_name,
                                             ordered_section_file_names)
            all_sections_soup.append(section_soup)

        cls.put_in_nice_bowl(all_sections_soup)

        return AdventureDoc(all_sections_soup)


if __name__ == '__main__':
    arguments = docopt.docopt(__doc__)
    source_directory = arguments["<source>"]
    adoc = AdventureDoc.from_directory(source_directory)

    with open(arguments["<destination>"], 'w') as f:
        f.write(str(adoc))
