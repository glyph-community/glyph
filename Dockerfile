FROM python:3.9
ARG REQUIREMENTS=requirements/release.txt

ENV PYTHONUNBUFFERED=1

RUN mkdir -p /opt
WORKDIR /opt

RUN echo Using $REQUIREMENTS
COPY $REQUIREMENTS requirements.txt
RUN pip3 install wheel
RUN pip3 install -r requirements.txt

COPY manage.py manage.py
COPY glyph glyph
COPY scripts/entrypoint.sh entrypoint.sh

ENTRYPOINT ["/opt/entrypoint.sh"]
CMD ["gunicorn", "-c", "/opt/glyph/configuration/gunicorn.py", "glyph.configuration.wsgi:application"]