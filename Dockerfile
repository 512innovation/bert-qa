FROM nvcr.io/ea-nvidia-ai-enterprise/tensorflow:21.02-tf1-py3

# Alternativelyl
# FROM nvcr.io/nvidia/tensorflow:21.05-tf1-py3

RUN pip install jupyterlab_nvdashboard

COPY . /workspace

ENTRYPOINT ["/bin/sh"]

CMD ["-c", "jupyter lab  --notebook-dir=/workspace --ip=0.0.0.0 --no-browser --allow-root --port=8888 --NotebookApp.token='' --NotebookApp.password='' --NotebookApp.allow_origin='*' --NotebookApp.base_url=${NB_PREFIX}"]
