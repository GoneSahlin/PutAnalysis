VENV = .venv

$(VENV): setup.cfg
	rm -rf $(VENV)
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -e .[dev]
	touch $(VENV)

.PHONY: lint
lint: $(VENV)
	-$(VENV)/bin/flake8 --exclude $(VENV) --max-line-length=88

.PHONY: format
format: $(VENV)
	-$(VENV)/bin/black --exclude $(VENV) .

.PHONY: test
test: $(VENV)
	-$(VENV)/bin/pytest

.PHONY: test-s
test-s: $(VENV)
	-$(VENV)/bin/pytest -s

.PHONY: clean
clean:
	rm -rf $(VENV)
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf *.eggs
	rm -rf *.egg
	rm -rf *.egg-info
	