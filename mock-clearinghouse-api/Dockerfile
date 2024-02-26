FROM python:3.11.7-slim-bookworm

WORKDIR /src

COPY requirements.txt /src/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /src

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]

#
# ENV PYTHONUNBUFFERED 1
# ENV APP_ROOT /src
# ENV CONFIG_ROOT /config
#
# RUN mkdir -p ${CONFIG_ROOT} \
#     mkdir -p ${APP_ROOT}
#
# RUN apt update && apt install -y --no-install-recommends \
#     git \
#     build-essential
#
# COPY requirements/prod.txt ${CONFIG_ROOT}/prod.txt
#
# RUN --mount=type=secret,id=GH_SECRET \
#     GH_SECRET=$(cat /run/secrets/GH_SECRET) pip install --no-cache-dir -r ${CONFIG_ROOT}/prod.txt
#
# WORKDIR ${APP_ROOT}
# ADD . ${APP_ROOT}
#
# EXPOSE 3000
#
# CMD ["uvicorn", "nirvana_eligible_sdk.main:app", "--host", "0.0.0.0", "--port", "3000", "--log-config", "log_config.json"]



