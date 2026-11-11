FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput && mkdir -p /data && chown -R 1001:0 /app /data && chmod -R g=u /app /data
USER 1001
EXPOSE 8000
ENTRYPOINT ["/bin/sh","/app/entrypoint.sh"]
CMD ["gunicorn","--bind","0.0.0.0:8000","--workers","2","django_concert.wsgi:application"]
