# AdventureDocs

Choose Your Own Adventure style software documentation from markdown.

Markdown source, when parsed, outputs to a single HTML page--no JavaScript.

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
  * Offer list options (anchor/id links) which lead to another section, e.g., "You're pretty much set, unless you'd like to
    go more in depth and explore..."
  * Offer progress bar

Things that'll be nice to have:

  * Index generation
  * Syntax highlighting
  * Templating
