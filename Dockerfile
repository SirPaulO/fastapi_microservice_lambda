FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1

WORKDIR /workdir

# Copy requirements.txt first for better cache on later pushes
COPY requirements.txt /workdir/requirements.txt
COPY requirements_lint.txt /workdir/requirements_lint.txt
COPY app/requirements.txt /workdir/app/requirements.txt
COPY tests/requirements.txt /workdir/tests/requirements.txt

# Install dependencies
RUN pip3 install -r requirements.txt -r requirements_lint.txt -r app/requirements.txt -r tests/requirements.txt

# Copy the rest of the code
COPY . /workdir/

EXPOSE 8000

CMD ["uvicorn", "--app-dir", "/workdir/app","main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
