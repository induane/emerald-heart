# Emerald Heart

Emerald Heart is an application for creating community directories and fostering community interaction.


## Makefile

This project uses a Makefile to orchestrate important tasks like creating a virtual environment, running 
unittests, etc...

A few useful ones:

* `make clean` - Clean build artifacts out of your project
* `make serve` - Install/update package and launch a local development server

You can see all available targets with the ``help`` target:

```shell
❯ make help
check-code           Check the code for linter errors
check-types          Run the ty typechecker
clean                Cleanup project workspace
css                  Generate output.css file
...
```

## Development Notes

JS & CSS are compiled into single files; the cost of setting up & tearing down http connections adds up,
particularly on cellular connections.

This package is quite conservative in many ways; it attempts to be easily managed and developed by a single individual 
if necessary. There is no react/vue/angular/aurelia/<insert-latest-framework-here> and all interaction is done via
``_hyperscript`` and ``htmx``. This preserves locality of behavior and allows a single developer to stay sane while
managing the complexity of the entire stack.
