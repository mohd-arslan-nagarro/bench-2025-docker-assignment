# ---------- Builder ----------
FROM python:3.14.3-alpine3.23 AS builder

WORKDIR /app

RUN pip install --upgrade pip==26.0 wheel==0.46.2 setuptools

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ---------- Runtime ----------
FROM python:3.14.3-alpine3.23

WORKDIR /app

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY --from=builder /install /usr/local
COPY . .

USER appuser

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "application:app"]

