# AGENTS.md

berklee_mls is a Django application for helping instructors provide meaningful feedback to students.

It is intentionally simple, a prototype MVP. It uses sqlite, django 6, HTMX, _HyperScript,
tailwind, etc... it has few dependencies intentionally. 

## Commands

```bash
# Task runner (preferred)
make check-code           ## Check the code for linter errors
make check-types          ## Run the ty typechecker
make clean                ## Cleanup project workspace
make createsuperuser      ## Create a superuser in the database
make css                  ## Generate output.css file
make deploy               ## Deploy to the application
make dump-auth            ## Update the auth fixture
make dump-fixtures        ## Update all fixtures
make freeze               ## List packages installed in the virtual environment
make generate-logos       ## Generate or regenerate logo files of various sizes
make git-clean            ## Cleanup git repository and remove dangling refs
make graph-dot            ## Generate a schema graph in dot format
make graph-png            ## Generate a schema graph in png format
make help                 ## Show this help
make js                   ## Build or rebuild berklee.min.js bundle
make loaddata             ## Load fixture data into the database
make node                 ## Install node packages
make qs                   ## Launch a local runserver without running migrations or loading fixtures
make serve                ## Launch a local runserver
make shell                ## Open an interactive Python shell in the projects context
make unittests            ## Run the projects unittest suite
make watch-css            ## Watch for changes to templates and rebuild CSS output as necessary
make wheel                ## Build a wheel distribution


# Run a single test method
export DJANGO_SETTINGS_MODULE=berklee_mls.settings.test && uv run django-admin test -v 2 -k test_name_here
```

## Javascript Bundle 
The file .Makefile.in has a variable JAVASCRIPT_FILES which lists files to be bundled and minified. It
also generates a source map. This is done with terser using the command:

```
make js
```

Which outputs:

berklee-mls.min.js
berklee-mls.min.js.map

There is no package.json or package-lock.json file.

## CSS Bundle

The file input.css found in src/berklee_mls/static/css is a config file for Tailwind. It lists CSS files
to be bundled into the minified CSS file. Sourcemaps are not supported. This is done using the command:

```
make css
```

Which outputs:

berklee-mls.min.css


## Python Code Style

### Formatting (use ruff formatter)
- **Line length**: 120 characters
- **Quotes**: Double quotes everywhere (`"like this"`)
- **Indentation**: 4 spaces

### Imports
Ordered by isort via Ruff: stdlib -> third-party -> first-party.
```python
import logging
from datetime import timedelta

from django.conf import settings
from django.db import models

from berklee_mls.utils.hash import hash_iter
```

No star imports outside settings files.

### Naming Conventions
- **UPPER_CASE**: constants, enum values, LOG ( `LOG = logging.getLogger(__name__)` )
- **snake_case**: functions, methods, variables, module names
- **PascalCase**: classes (models, views, services, serializers)
- 
### Type Hints
Python-native type hints: `str | None`, `list[dict]`, `-> HttpResponse`. No separate type files.


### Logging
```python
import logging

LOG = logging.getLogger(__name__)

LOG.info('Do %s: %s', val_1, val_2)
```

- Use `%s` formatting instead of f-strings
- Do NOT use the modulus operator for string formatting in log messages

### Primary Keys
Prefer to use UUID4 for all primary keys.

```python
import uuid
from django.db import models

id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
```

## Testing

### Unit Tests (Django native testrunner -- `manage.py test`)
- **Utility functions**: Use `unittest.TestCase`
- **Testing models and views**: Use `django.test.TestCase`
- Use `self.assertEqual`, etc.. -- never a bare `assert`
- Never suggest or use pytest in any form


### File Layout
```
tests/test_*.py           # Unit tests 
```

## User Interface

- Do not add any additional javascript
- Async get/post/etc... should be handled via HTMX (already bundled in the application js payload)
- Additional interface interactivity should be done with _HyperScript (already bundled in the application js payload)
- Tailwind should be used for styling
- When feasible, follow existing templates for style


## Anti-Patterns (stuff to please avoid)
- Avoid huge classes (split them into smaller, focused classes)
- Utility functions should be small and easily tested without side effects or mocks
- Parameterize functions as little as possible
- No mutable default arguments like lists or dictionaries
- Don't store data in models when it can be computed from other data (expose computed data as model methods/properties
- Use logging instead of print
- Make sure datetimes have a timezone - use UTC when possible
- Avoid storing datetime values in any timezone aside from UTC (convert to UTC before storing)
- Avoid computing values that don't change (i.e. x = 60 * 5 --> instead use x = 300 )
- No dependency injection (use Django's built-in dependency injection when relevant, otherwise avoid alltogether)
- Don't use {#  and #} for multi-line comments in Django templates (they don't work that way)
