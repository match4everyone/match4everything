FROM ubuntu:18.04

RUN apt-get update && apt-get install -y python3 python3-pip libpq-dev gettext

WORKDIR /backend
COPY requirements.txt /backend/requirements.txt
RUN pip3 install -r requirements.txt
COPY requirements.prod.txt /backend/requirements.prod.txt
RUN pip3 install -r requirements.prod.txt

COPY . .

RUN python3 manage.py makemessages --no-location
RUN python3 manage.py compilemessages
RUN python3 manage.py collectstatic --no-input
# Change permissions on run/ in case app is later run by non-root user
# and delete log files as these are created during the above commands when django loads the configuration
# and will be created non writeable by others than root
RUN rm -v run/log/* && chmod a+rwX run/log && chmod a+rwX backups

EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
