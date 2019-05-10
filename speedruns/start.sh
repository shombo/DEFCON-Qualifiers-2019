docker build -t speedrun .
echo -e "\nStarting container\n"
docker run -it --privileged -v `pwd`:/mnt speedrun
