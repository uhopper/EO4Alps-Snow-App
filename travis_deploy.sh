echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

VERSION=`awk -F'[=&]' '{print $2}' < . edc_ogc/__init__.py  | tr -d '"'`

if [ $TRAVIS_BRANCH == "master" ]; then
    docker tag "$REGISTRY_IMAGE:tmp_build" "$REGISTRY_IMAGE:latest"
    docker tag "$REGISTRY_IMAGE:tmp_build" "$REGISTRY_IMAGE:$VERSION"
    docker push "$REGISTRY_IMAGE:latest"
    docker push "$REGISTRY_IMAGE:$VERSION"
else
    docker tag "$REGISTRY_IMAGE:tmp_build" "$REGISTRY_IMAGE:$TRAVIS_COMMIT"
    docker push "$REGISTRY_IMAGE:$TRAVIS_COMMIT"
fi
