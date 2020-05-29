sudo docker rmi melth_image --force;
sudo docker build -t melth .;
sudo docker rm melth --force;
sudo docker run --name melth --restart "always" -d melth_image;