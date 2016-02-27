# AdventureDoc Notes

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
