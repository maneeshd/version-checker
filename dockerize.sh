echo ""
echo "Dockerizing the API Sevrer..."
echo ""
echo "Building docker image..."
echo ""
docker build --compress --force-rm --tag "maneeshd/version-checker:latest" .
echo ""
echo "Docker image built"
echo ""
echo "Pushing the docker image to DockerHub..."
echo ""
docker push --disable-content-trust=false maneeshd/version-checker:latest
echo ""
echo "Pushed the docker image to DockerHub."
echo ""
echo "Running the image..."
echo ""
docker run --rm -p 8000:8000 --name version_checker maneeshd/version-checker