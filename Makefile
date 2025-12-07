include .Makefile.in

node: ## Install node packages
	$(NODE_INSTALL)

.PHONY: js
js: node  ## Build or rebuild emerald.min.js bundle
	- @rm -f $(MAKEFILE_DIR)/static/js/emerald.min.js
	- npx terser $(JAVASCRIPT_FILES) --mangle --validate --toplevel --safari10 --compress --output $(MAKEFILE_DIR)/src/emerald_heart/static/js/emerald.min.js --source-map "url='emerald.min.js.map',root='/static/js',base='static/js'"

.PHONY: css
css: node  ## Generate output.css file
	- npx tailwindcss --minify --input $(MAKEFILE_DIR)/src/emerald_heart/static/css/input.css --output $(MAKEFILE_DIR)/src/emerald_heart/static/css/emerald.min.css

.PHONY: css
watch-css: node  ## Watch for changes to templates and rebuild CSS output as necessary
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

.PHONY: unittests
unittests:  ## Run the projects unittest suite
	$(TEST_CONTEXT) uv run django-admin test -v 2

.PHONY: migrate
migrate:  # Run the database migrations
	- $(WITH_CONTEXT) uv run django-admin migrate --noinput

.PHONY: migrations
migrations:  # Generate database migrations
	$(WITH_CONTEXT) uv run django-admin makemigrations

.PHONY: check-types
check-types:  ## Run the ty typechecker
	uv run --group dev ty check --exclude=**/utils/image.py

.PHONY: format-code
format-code:  # Run the ruff code formatter
	@$(IN_ENV) ruff format $(MAKEFILE_DIR)/src/ $(MAKEFILE_DIR)/tests/ $(MAKEFILE_DIR)/resources/generate_images.py
	@$(IN_ENV) ruff check --fix $(MAKEFILE_DIR)/src/ $(MAKEFILE_DIR)/tests/ $(MAKEFILE_DIR)/resources/generate_images.py

.PHONY: check-code
check-code:  ## Check the code for linter errors
	$(IN_ENV) ruff check $(MAKEFILE_DIR)/src/ $(MAKEFILE_DIR)/tests/ $(MAKEFILE_DIR)/resources/generate_images.py

.PHONY: shell
shell:  ## Open an interactive Python shell in the projects context
	$(WITH_CONTEXT) uv run django-admin shell -v 2

.PHONY: qs
qs:  ## Launch a local runserver without running migrations or loading fixtures
	$(WITH_CONTEXT) uv run django-admin runserver --verbosity 3 $(IP):$(PORT)

.PHONY: serve
serve: migrate loaddata  ## Launch a local runserver
	#
	$(WITH_CONTEXT) uv run django-admin runserver --verbosity 3 $(IP):$(PORT)

.PHONY: dump-auth
dump-auth:  ## Update the auth fixture
	@rm -rf $(MAKEFILE_DIR)/src/emerald_heart/fixtures/auth.json
	$(WITH_CONTEXT) uv run django-admin dumpdata auth.Group emerald_heart.User --indent=4 > $(MAKEFILE_DIR)/src/emerald_heart/fixtures/auth.json

.PHONY: loaddata
loaddata:  ## Load fixture data into the database
	$(WITH_CONTEXT) uv run django-admin loaddata $(FIXTURE_FILES)

.PHONY: freeze
freeze:  ## List packages installed in the virtual environment
	@uv pip freeze --color auto

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
