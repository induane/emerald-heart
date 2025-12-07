include .Makefile.in

.PHONY: check-types
check-types:  ## Run the ty typechecker
	@uvx ty check --exclude=**/utils/image.py

.PHONY: css
css: node_modules  ## Generate output.css file
	- npx tailwindcss --minify --input $(MAKEFILE_DIR)/src/emerald_heart/static/css/input.css --output $(MAKEFILE_DIR)/src/emerald_heart/static/css/emerald.min.css

.PHONY: css
watch-css: node_modules  ## Watch for changes to templates and rebuild CSS output as necessary
	npx tailwindcss --minify --watch --input $(MAKEFILE_DIR)/src/emerald_heart/static/css/input.css --output $(MAKEFILE_DIR)/src/emerald_heart/static/css/emerald.min.css

.PHONY: generate-logos
generate-logos:  ## Generate or regenerate logo files of various sizes
	$(WITH_CONTEXT) uv run python resources/generate_images.py
	mv resources/apple-* src/emerald_heart/static/images/
	mv resources/favicon* src/emerald_heart/static/images/
	mv resources/ms-icon-* src/emerald_heart/static/images/
	- @find resources -name 'apple*' -delete
	- @find resources -name 'favicon*' -delete
	- @find resources -name 'ms-icon*' -delete

node: $(NODE_DIR)  ## Install node packages
	$(NODE_INSTALL)

.PHONY: unittests
unittests:  ## Run the projects unittest suite
	$(TEST_CONTEXT) uv run django-admin test -v 2

.PHONY: migrate
migrate:  # Run the database migrations
	- $(WITH_CONTEXT) uv run django-admin migrate --noinput

.PHONY: migrations
migrations:  # Generate database migrations
	$(WITH_CONTEXT) uv run django-admin makemigrations

.PHONY: format-code
format-code:  # Run the ruff code formatter
	@$(IN_ENV) ruff format $(MAKEFILE_DIR)/src/ $(MAKEFILE_DIR)/tests/ $(MAKEFILE_DIR)/resources/generate_images.py
	@$(IN_ENV) ruff check --fix $(MAKEFILE_DIR)/src/ $(MAKEFILE_DIR)/tests/ $(MAKEFILE_DIR)/resources/generate_images.py

.PHONY: check-code
check-code:  ## Check the code for linter errors
	$(IN_ENV) ruff check $(MAKEFILE_DIR)/src/ $(MAKEFILE_DIR)/tests/ $(MAKEFILE_DIR)/resources/generate_images.py

.PHONY: js
js:  ## Build or rebuild emerald.min.js bundle
	- @rm -f $(MAKEFILE_DIR)/static/js/emerald.min.js
	- npx terser $(JAVASCRIPT_FILES) --mangle --validate --toplevel --safari10 --compress --output $(MAKEFILE_DIR)/src/emerald_heart/static/js/emerald.min.js --source-map "url='emerald.min.js.map',root='/static/js',base='static/js'"

.PHONY: shell
shell:  ## Open an interactive Python shell in the projects context
	$(WITH_CONTEXT) uv run django-admin shell -v 2

.PHONY: qs
qs:  ## Launch a local runserver without running migrations or loading fixtures
	$(WITH_CONTEXT) uv run django-admin runserver --verbosity 3 $(IP):$(PORT)

.PHONY: serve
serve:  ## Launch a local runserver
	#
	$(WITH_CONTEXT) uv run django-admin runserver --verbosity 3 $(IP):$(PORT)

.PHONY: clean
clean:  ## Cleanup project workspace
	- @git clean -dfX >> /dev/null 2>&1
	- @rm -rf .venv*
	- @rm -rf node_modules

.PHONY: git-clean
git-clean:  ## Cleanup git repository and remove dangling refs
	- @git fsck
	- @git reflog expire --expire=now --all
	- @git repack -ad
	- @git prune
