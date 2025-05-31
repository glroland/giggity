include config.env
export

install:
	pip install -r web/requirements.txt
	pip install -r api/requirements.txt

run.web:
	cd web/src && streamlit run app.py --server.address 0.0.0.0 --server.port 8501

run.api:
	cd api/src && flask run --host 0.0.0.0 --port 8080
