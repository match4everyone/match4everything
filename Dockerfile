FROM node:12-alpine AS frontendbuilder
WORKDIR /frontend
COPY /frontend/package.json /frontend/package-lock.json ./
RUN ["npm", "install"]

# Build the javascript bundles in the intermediate stage
COPY frontend ./
RUN [ "npm" , "run", "build" ]

# CMD only used in development context.
CMD [ "npm" , "run", "dev" ]
# If started using docker-compose up:
# docker-compose.yml + docker-compose.override.yml are used and a frontend container is started running the CMD
# (see docker-compose.override.yml target parameter for service frontend)
#
# If started using docker-compose up -f docker-compose.yml -f docker-compose.prod.yml:
# docker-compose.yml + docker-compose.prod.yml are used *without* docker-compose.override.yml
# frontend container is never started but the results from npm run build above are copied into the backend container
# during the second build stage (https://docs.docker.com/develop/develop-images/multistage-build/)


FROM ubuntu:18.04 AS backend
RUN apt-get update && apt-get install -y python3 python3-pip libpq-dev gettext

WORKDIR /backend
COPY backend/requirements.txt /backend/requirements.txt
RUN pip3 install -r requirements.txt
COPY backend/requirements.prod.txt /backend/requirements.prod.txt
RUN pip3 install -r requirements.prod.txt

# Copy the JS Bundle from the intermediate stage over into the backend container
# Important: Do this before collecting static, otherwise the bundles won't be found
COPY --from=frontendbuilder frontend/dist /frontend/dist
COPY backend .

RUN python3 manage.py makemessages --no-location  &&\
    python3 manage.py compilemessages             &&\
    python3 manage.py collectstatic --no-input
# Change permissions on run/ in case app is later run by non-root user
# and delete log files as these are created during the above commands when django loads the configuration
# and will be created non writeable by others than root
RUN rm -v run/log/* && chmod a+rwX run/log && chmod a+rwX backups

EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
