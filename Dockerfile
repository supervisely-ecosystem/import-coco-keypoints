FROM supervisely/base-py-sdk:6.72.49

COPY dev_requirements.txt dev_requirements.txt
RUN pip install -r dev_requirements.txt