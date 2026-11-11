# Back-end-Development-Capstone

## Project: Djirection — band website

Django band website by nrnbekovv, built from the IBM Developer Skills Network capstone starter.
Includes home, songs with lyrics modals, photo gallery, registration/login/logout, concerts, per-user RSVP and Django administration.
Songs and photos are fetched from the separate Flask microservices; there is no silent sample-data fallback.

### Run locally
Use Python 3.12. Install `requirements.txt`, set SONGS_URL and PICTURES_URL to the running services, then:
```
python manage.py migrate
python manage.py seed_concerts
python manage.py createsuperuser
python manage.py collectstatic --noinput
python manage.py runserver
```
Set DJANGO_SECRET_KEY to a unique secret in deployments. Configure DJANGO_ALLOWED_HOSTS (comma-separated host names) and DJANGO_CSRF_TRUSTED_ORIGINS (comma-separated HTTPS origins). DJANGO_DEBUG defaults to off. DJANGO_DB_PATH optionally selects a persistent SQLite file.

### Deployment
Docker runs Gunicorn on port 8000 and WhiteNoise serves static assets. The entrypoint applies migrations and seeds the sample concert schedule idempotently. Kubernetes manifests use a persistent volume and a Secret supplied at deploy time, never a committed password. This lab deployment uses one replica with SQLite.

### Related repositories
- https://github.com/nrnbekovv/Back-End-Development-Pictures
- https://github.com/nrnbekovv/Back-End-Development-Songs

### Validation
`python manage.py test` checks login, authentication boundaries and RSVP persistence. The original UI assets and templates are retained from the IBM starter.
