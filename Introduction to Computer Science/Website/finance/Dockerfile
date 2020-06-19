FROM tiangolo/uwsgi-nginx-flask
ENV STATIC_URL /static
ENV STATIC_PATH /mnt/e/Education/Online Computer Sience degree/Introduction to Computer Science/Website/finance
COPY ./requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt