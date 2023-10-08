FROM python:3.9-slim
RUN  apt-get -yq update && \
     apt-get -yqq install git ssh

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ /Asia/Kolkata
RUN mkdir -p /code
RUN mkdir -p /var/log/swiggy_logs/

RUN mkdir -p /root/.ssh && \
    chmod 0700 /root/.ssh && \
    ssh-keyscan github.com > /root/.ssh/known_hosts

ADD ssh_prv_key /root/.ssh/id_rsa
RUN chmod 600 /root/.ssh/id_rsa

WORKDIR /code
COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ /code
RUN chmod 755 -R /code
RUN chmod 777 -R /code/
RUN chmod 777 -R /var/log/credgenics_logs/

RUN rm ssh_prv_key && \
    rm /root/.ssh/id_rsa

EXPOSE 8000

CMD uvicorn server:app --host 0.0.0.0 --port 8000 --no-access-log
