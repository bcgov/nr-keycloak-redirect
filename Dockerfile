FROM python:3.10

# Upgrade pip
RUN pip install --upgrade pip

# Set up non-root user
ARG USER=python_runner
RUN useradd ${USER} && \
    mkdir -p /home/${USER} && \
    chown -R ${USER}:${USER} /home/${USER}

# Set up app
USER ${USER}
WORKDIR /home/${USER}
COPY . .
RUN pip install -r requirements.txt --no-warn-script-location
RUN chmod +x entrypoint.sh
# Set entrypoint, will pass params
ENTRYPOINT [ "./entrypoint.sh" ]
