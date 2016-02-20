# AdventureDocs

Choose Your Own Adventure style software documentation from markdown.

Markdown source, when parsed, outputs to a single HTML page.

## The Idea

Since this repo is still in concept phase, I thought I'd explain the concept!

The problems:

  * It is difficult to maintain a monolith of documentation
  * It is hard to read a monolith of documentation
  * Documentation varies per use case, specific needs, platforms, etc
  * Documentation can be intimidating
  * No clear distinguishing UX for required and optional sections
  
The solution:

  * Be like a software documentation static site generator version of Google Forms (choose your own adventure!)
  * Each markdown file is a `<section>` with a respective `id` (it's filename).
    This is how we'll use CSS to show/hide elements, links to other sections, etc.
  * Offer list options (anchor/id links) which lead to another section, e.g., "You can run this with VirtualBox or VMWare. 1. Virtualbox 2. VMWare"
  * Amazing markdown syntax additions
  * Offer progress bar
  * A way to show/hide things *within* the section
  * Optional "header images" per section--iconography is powerful!

Things that'll be nice to have:

  * Index generation
  * Syntax highlighting
  * Templating

### An example

In `first_step.md`:

```markdown
# Getting Started

You'll want to install our software like this:

CONTEXT_EXAMPLE:

  * install_on_osx.md
  * install_on_linux.md

Once you're done you can wrap up, or if you wanna develop we have specific
instructions for that!

NEXT_SECTION:

   * wrap_up.md
   * develop_start.md
```

## Relevant Resources:

  * http://pythonhosted.org/Markdown/reference.html
