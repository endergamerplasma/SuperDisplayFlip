if not exist .venv (
	python setup.py
	python -m venv .venv
	.venv\Scripts\activate
	pip install -r requirements.txt
)
