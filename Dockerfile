FROM python:3.11-slim
ENV PYTHONUNBUFFERED 1
WORKDIR /app

COPY pyproject.toml .

RUN pip3 install poetry
# already in a virtual environment by using a docker image, there's no need to build another environment
RUN poetry config virtualenvs.create false

# Installs all the required packages minus the development packages
RUN poetry install --only main

COPY kub /app/src
COPY data .
EXPOSE 5000
# Run the application in the port 5000
CMD ["uvicorn", "src.main:app", "--workers", "1", "--host", "0.0.0.0", "--port", "5000"]
