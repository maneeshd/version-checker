set -e

echo ""
echo "Dockerizing the API Sevrer..."
echo ""
echo "Building docker image..."
echo ""
docker build --file Dockerfile --compress --force-rm --tag "maneeshd/version_checker:latest" .
echo ""
echo "Docker image built"
echo ""
echo "Pushing the docker image to DockerHub..."
echo ""
docker push maneeshd/version_checker:latest
echo ""
echo "Pushed the docker image to DockerHub."
echo ""
# echo "Running the image..."
# echo ""
# docker run --rm -p 8000:8000 --name version_checker maneeshd/version_checker:latest