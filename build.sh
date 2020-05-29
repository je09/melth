sudo docker rmi melth_image --force;
sudo docker build -t melth_image .;
sudo docker rm melth --force;
sudo docker run --name melth -p 8003:8003 --restart "always" -d melth_image;
