
FROM ubuntu:latest

# Open port for reporting dashboard
EXPOSE 8675

RUN mkdir "/pytest_framework"
WORKDIR "/pytest_framework"
# Copy Testing Framework to container
COPY ./* /pytest_framework/
# Remove local data from container
RUN rm -rf /pytest_framework/.git /pytest_framework/logs

# Install packages without interactive prompts
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get -y install \
    default-jre-headless libxml2 libpq-dev vim nano zsh net-tools wget curl dnsutils iputils-ping

# Install packages and install additional tools / software
RUN apt-get update && apt-get install -y apt-utils python3 python3-pip build-essential python-dev
# Install mySQL dependencies
RUN apt-get -y install python3-mysqldb
# Create Symbolic Link for python3 = python
RUN ln -nsf /usr/bin/python3 /usr/bin/python
# Install Python dependencies
RUN python -m pip install -r /pytest_framework/requirements.txt

# Install allure
RUN curl -o allure-2.13.8.tgz -OLs https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.13.8/allure-commandline-2.13.8.tgz
RUN tar -zxvf allure-2.13.8.tgz -C /opt/
RUN ln -s /opt/allure-2.13.8/bin/allure /usr/bin/allure

ENTRYPOINT ["zsh"]