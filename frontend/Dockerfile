FROM node:12-alpine

WORKDIR /app
COPY package.json package-lock.json /app/
RUN ["npm", "install"]

COPY . /app/
ENTRYPOINT [ "npm" , "run", "build" ]
