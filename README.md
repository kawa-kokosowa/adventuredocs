# AdventureDocs

Choose Your Own Adventure style software documentation from markdown.

Markdown source, when parsed, outputs to a single HTML page.

Demo: http://hypatia-software-org.github.io/adventuredocs/

## Test it out!

We've included a demo! Checkout the `testdocs/` directory! It
contains markdown files which represent sections, and an `ORDER`
file which specifies the default order of the sections.

All you have to do to get started is:

  1. `pip install -r requirements.txt`
  2. `python adocs.py testdocs outputfile.html`

Then you can view `outputfile.html` in your web browser!

## Misc. Notes

This repository is very conceptual and is in its infancy.

What we want to solve:

  * Difficulty of maintaining a monolith of documentation
  * Difficulty of _reading_ a monolith of documentaiton
  * Variablity of documentation, instructions which depend on
    specific needs, use cases, platforms, etc.
  * Intimidation-factor of documentation
  * Some other stuff I'm forgetting to put in here!

The main ways we'll solve those problems:

  * CYOA-style static stite generator for software documentation!
  * Each markdown file is a `<section>` with a respective `id` (it's filename).
  * An `ORDER` file which specifies the default order
  * `NEXT_SECTION:` if in its own paragraph in markdown, the proceeding
    list will be transformed into a list of links to other sections!
  * Progress bar!
  * A way to set variables/user settings, e.g., "using_linux" to display content
    based on how a question was answered.
  * A way to show/hide things *within* the section
