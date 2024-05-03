VENV = .venv

$(VENV): requirements.txt
	rm -rf $(VENV)
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt
	touch $(VENV)

.PHONY: lint
lint: $(VENV)
	-$(VENV)/bin/flake8 --exclude $(VENV)

.PHONY: clean
clean:
	rm -rf $(VENV)
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf *.eggs
	rm -rf *.egg
	rm -rf *.egg-info
	