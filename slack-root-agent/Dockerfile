FROM python:3.14-slim

RUN pip install --no-cache-dir uv==0.8.13

WORKDIR /code

COPY ./pyproject.toml ./README.md ./uv.lock* ./

COPY . .

RUN uv sync --frozen

EXPOSE 8080

CMD ["uv", "run", "python", "main.py"]