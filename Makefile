.DEFAULT_GOAL := default
#################### PACKAGE ACTIONS ###################
reinstall_package:
	@pip uninstall -y api || :
	@pip install -e .
run_api:
	uvicorn api.api:app --reload

reset_local_files:
	rm -rf ${ML_DIR}
	mkdir -p ~/.lewagon/mlops/data/
	mkdir ~/.lewagon/mlops/data/raw
	mkdir ~/.lewagon/mlops/data/processed
	mkdir ~/.lewagon/mlops/training_outputs
	mkdir ~/.lewagon/mlops/training_outputs/metrics
	mkdir ~/.lewagon/mlops/training_outputs/models
	mkdir ~/.lewagon/mlops/training_outputs/params
#run_preprocess:
#	python -c 'from taxifare.interface.main import preprocess; preprocess()'

#run_train:#
#	python -c 'from taxifare.interface.main import train; train()'

#run_pred:
#	python -c 'from taxifare.interface.main import pred; pred()'

#run_evaluate:
#	python -c 'from taxifare.interface.main import evaluate; evaluate()'

#run_all: run_preprocess run_train run_pred run_evaluate

#run_workflow:
#	PREFECT__LOGGING__LEVEL=${PREFECT_LOG_LEVEL} python -m taxifare.interface.workflow
