#To run the code locally -
#build mysql image, go to the mysql-image-code folder and run -
docker build -t mysql-with-schema .

#build application image - 
docker build -t  flask-app-image .

#Create a docker network so that the application can talk to mysql container

docker network create application-network

#Run mysql container in the same network -
docker run -d \
  --name mysql \
  --network app-network \
  -e MYSQL_ROOT_PASSWORD=root123 \
  -e MYSQL_DATABASE=database-1 \
  -v mysql_data:/var/lib/mysql \
  mysql-with-schema

#Run flask app into the same network and pass the environment variables-
docker run -d \
  --name flask-app \
  --network app-network \
  -p 5000:5000 \
  -e DB_HOST=mysql \
  -e DB_USER=root \
  -e DB_PASSWORD=root123 \
  -e DB_NAME=database-1 \
  flask-app-image

#to run it using  docker-compose you can use below command

  docker compose pull
  
  docker compose up

#But one of the image is private so docker-compose won't be able to pull that image without access

