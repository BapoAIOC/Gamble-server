FROM python:3.8.2

# Install the dependencies.
RUN apt-get update

# Update PIP
RUN pip3 install --upgrade pip

# Create directory for code.
RUN mkdir -p /opt/server/logs
COPY code/requirements.txt /opt/server/requirements.txt

# Install pip requirements
WORKDIR /opt/server
RUN pip install -r requirements.txt

# Copy over the rest of the code
COPY code/* /opt/server/

# Add the entrypoint.
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# run main.py on entry
CMD [ "/entrypoint.sh" ]