def change_soup(adventuredoc, section):
    """Create the HTML for the provided file contents!

    Should maybe have the callback....

    Returns:
        BeautifulSoup: --

    """

    soup = section.soup
    total_number_of_sections = len(adventuredoc.sections)

    # Section Progress/Position
    progress = section.soup.new_tag("progress")
    progress['value'] = section.index + 1
    progress['max'] = total_number_of_sections
    soup.insert(0, progress)

    # If there's a next section add the "next section" link!
    try:
        next_section_name = adventuredoc.sections[section.index + 1].name
        link = soup.new_tag("a", href="#" + next_section_name)
        link["class"] = "next"
        link.string = "Next Section"
        soup.append(link)

    except IndexError:
        pass

    section_wrapper = soup.new_tag("section")
    section_wrapper["id"] = section.name

    section_wrapper.append(soup)

    return section_wrapper

