def change_soup(adventuredoc, section):
    soup = section.soup

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

        if ((previous_paragraph is not None) and
            (previous_paragraph.text == adventuredoc.SECTION_CHOICE_KEYWORD)):


            # Create a <nav> container and put a paragraph
            # "Jump to..." inside it.
            jump_to_nav = soup.new_tag("nav", **{'class': "jumpto"})
            paragraph = soup.new_tag("p")
            paragraph.string = "Jump to..."
            jump_to_nav.append(paragraph)

            list_of_options = soup.new_tag("ul")

            # We're going to make each LI's contents a link
            # to the markdown file it specifies!
            for li in ul.find_all("li"):
                section_name, __ = li.string.rsplit('.', 1)
                link = soup.new_tag("a", href="#%s" % section_name)
                link.string = section_name

                new_list_item = soup.new_tag("li")
                new_list_item.append(link)

                list_of_options.append(new_list_item)

            # we created a new list, remove the old one!
            ul.replaceWith('')

            # put everything in our nice jumpto nav
            # container
            jump_to_nav.append(list_of_options)
            previous_paragraph.replaceWith(jump_to_nav)
