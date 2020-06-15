FROM node:12-alpine

WORKDIR /frontend
COPY package.json package-lock.json /frontend/
RUN ["npm", "install"]

COPY . /frontend/
ENTRYPOINT [ "npm" , "run", "build" ]
