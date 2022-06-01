FROM python:3.9.2
ENV PYTHONUNBUFFERED 1
ENV WEB_DIR /baul  
RUN mkdir ${WEB_DIR}
# Actualizacion de los 'sources' a la ultima version
RUN apt-get update
# Instalar los paquetes del sistema necesarios para python
RUN apt-get install -qy python \
                        python-dev \
                        python-pip \
                        python-setuptools \
                        build-essential
# Instalar algunas utilidades extras (opcional)
RUN apt-get install -qy vim \
                        wget \
                        net-tools \
                        git

# Instalamos resto aplicaciones
RUN apt-get install -qy nginx \
                        supervisor                     
WORKDIR ${WEB_DIR}
COPY . ${WEB_DIR} 
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["gunicorn","-c","conf.py","--bind",":8000","--chdir","baul","baul.wsgi.py:application",python manage.py migrate,python manage.py runserver 0:8000]
