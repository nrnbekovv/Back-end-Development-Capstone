# Module 3 milestone

This runnable snapshot reproduces the early Django lab before microservice integration: one local song and the lab's single photo record. The final application uses all records from the deployed services.

Run against the built Django image:

```bash
docker run -d --name django-lab-stage -p 8001:8000 -v "$PWD/lab-stage/views.py:/app/concert/views.py:ro" -e DJANGO_DB_PATH=/data/lab.sqlite3 us.icr.io/sn-labs-fieriertapes/djangoserver:2
```

Open port 8001 through the Skills Network toolbox. The screenshots django-app-browser, django-song-modal and django-photos were captured from this running milestone. Deployment screenshots use the final Kubernetes application on port 8000.
