ESTANDAR ?= ../estandares-modelos

datos:
	python src/datos.py

modelo:
	python src/modelo.py --seed 20261017

reportes:
	python src/reportes.py

verificar:
	python $(ESTANDAR)/tools/verificar.py . --hash

sellar:
	python $(ESTANDAR)/tools/verificar.py --sellar .
