#!/bin/sh

set -e

# Get secrets + build secrets file
python ./git-repo/ci/scripts/get_secrets.py $SECRETS_PATH 'export {{ n }}="{{ v }}"'

# Set version
export VERSION=`cat ./version/version`

# Replace secret placeholders with actual secrets from SSM
python ./git-repo/ci/scripts/variable_replacer.py ./git-repo/ci/$COMPOSE_FILE \
    VERSION $VERSION \
    BARCLAYS_ADAPTER_AWS_ACCESS_KEY_ID $BARCLAYS_ADAPTER_AWS_ACCESS_KEY_ID \
    BARCLAYS_ADAPTER_AWS_SECRET_ACCESS_KEY $BARCLAYS_ADAPTER_AWS_SECRET_ACCESS_KEY

# Create docker-swarm PEM for deployment
touch docker_swarm_key.pem
echo $DOCKER_SWARM_KEY | sed -e 's/\(KEY-----\)\s/\1\n/g; s/\s\(-----END\)/\n\1/g' | sed -e '2s/\s\+/\n/g' > docker_swarm_key.pem
chmod 600 docker_swarm_key.pem

# Set deploy requirements
commandstr="docker stack deploy -c ./git-repo/ci/docker-compose-staging.yml $SERVICE_NAME --with-registry-auth"
ssh -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null -i ./docker_swarm_key.pem -NL localhost:2376:/var/run/docker.sock docker@$DOCKER_SWARM_HOSTNAME &
export DOCKER_HOST="localhost:2376"
sleep 3
docker login -u $DOCKER_HUB_USER -p $DOCKER_HUB_PASSWORD

# Run deployment
$commandstr
exitcd=$?
if [ $exitcd == 0 ]; then
    echo "deploy success"
else
    echo "error! exit code: $exitcd"
    exit 1
fi

# clean up
set -x

echo "$SERVICE_NAME deployed..."
