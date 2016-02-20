# AdventureDocs

Choose Your Own Adventure style software documentation from markdown.

Markdown source, when parsed, outputs to a single HTML page.

## Test it out!

We've included a demo! All you have to do to get started is:

  1. `pip install -r requirements.txt`
  2. `python adocs.py source_directory outputfile.html`

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

How we're gonna solve them:

  * CYOA-style static stite generator for software documentation! Inspired by Google Forms.
  * Each markdown file is a `<section>` with a respective `id` (it's filename).
  * An `ORDER` file which specifies the default order

  * Offer list options (anchor/id links) which lead to another section, e.g., "You can run this with VirtualBox or VMWare. 1. Virtualbox 2. VMWare"
  * Amazing markdown syntax additions
  * Offer progress bar
  * A way to show/hide things *within* the section
  * Optional "header images" per section--iconography is powerful!

Things that'll be nice to have:

  * Syntax highlighting
  * Templating
