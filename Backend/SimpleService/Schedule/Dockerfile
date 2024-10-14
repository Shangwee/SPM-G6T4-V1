FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./schedule.py .
COPY ./schedule_test.py .
CMD [ "python", "./schedule.py" ]