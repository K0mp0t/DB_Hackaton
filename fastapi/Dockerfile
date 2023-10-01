FROM python:3.10-slim
# TODO: Я понятия не имею что мне тут чат нагенерил
# Install system packages
RUN apt-get update && \
    apt-get install -y \
        apt-transport-https \
        build-essential \
        cmake \
        curl \
        gcc \
        g++ \
        git \
        libpq-dev \
        python3-dev \
        tree \
        sudo \
        unzip \
        wget \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY . /home/DB_Hackaton_API
RUN pip install --no-cache-dir --ignore-installed -r /home/DB_Hackaton_API/requirements.txt

# Configure default user name and ID
ARG USER_ID="1000"
ENV USER_ID=${USER_ID}
ENV USER_NAME="fastapi"

RUN useradd -m ${USER_NAME} -u ${USER_ID} && \
    echo "${USER_NAME}:${USER_NAME}" | chpasswd ${USER_NAME} && \
    echo "${USER_NAME} ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/${USER_NAME} && \
    chmod 0440 /etc/sudoers.d/${USER_NAME} && \
    chown -R ${USER_NAME} /home
USER ${USER_NAME}

# Configure workdir
WORKDIR /home/DB_Hackaton_API
# Configure PYTHONPATH environment variable
ENV PYTHONPATH=/home/DB_Hackaton_API

# Launch uvicorn server with FastAPI application on start up
CMD uvicorn app:app --app-dir fastapi --reload  --host 0.0.0.0 --port 5000