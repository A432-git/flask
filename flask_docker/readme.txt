Go to the project directory (in where your Dockerfile is, containing your app directory)
Build your Flask image:
docker build -t myimage .
Run a container based on your image:
docker run -d --name mycontainer -p 80:80 myimage