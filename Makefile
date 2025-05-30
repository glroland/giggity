include config.env
export

install:
	pip install -r web/requirements.txt

run.web:
	cd web/src && streamlit run app.py
