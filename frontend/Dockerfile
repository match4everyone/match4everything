FROM node:12-alpine

# This Dockerfile is only used to run the development webpack from docker-compose.override.yml
# The build process for the production image is a intermediate stage in the root Dockerfile

WORKDIR /frontend
COPY package.json package-lock.json /frontend/
RUN ["npm", "install"]

COPY . /frontend/
CMD [ "npm" , "run", "dev" ]
