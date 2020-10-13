FROM python:3.9
ARG REQUIREMENTS=requirements/release.txt
ARG PORT=5000

ENV PYTHONUNBUFFERED=1

RUN mkdir -p /opt
WORKDIR /opt

RUN apt-get update && apt-get install -y \
    libmemcached-dev

RUN echo Using $REQUIREMENTS
COPY $REQUIREMENTS requirements.txt
RUN pip3 install wheel
RUN pip3 install -r requirements.txt

COPY manage.py manage.py
COPY glyph glyph
COPY scripts/entrypoint.sh entrypoint.sh

EXPOSE ${PORT}
ENTRYPOINT ["/opt/entrypoint.sh"]
CMD ["gunicorn", "-c", "/opt/glyph/configuration/gunicorn.py", "glyph.configuration.wsgi:application"]