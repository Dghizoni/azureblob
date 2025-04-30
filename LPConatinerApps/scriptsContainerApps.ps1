# CRIANDO A IMAGEM DOCKER

docker build -t landpage-projeto:latest .

docker run -d -p 8084:80 landpage-projeto:latest


# CRIANDO CONTAINER APP NA AZURE
az login

rc_name=nome_do_resourcegroup
rc_location=local_do_resourcegroup

# cria o resource group
az group create --name {rc_name} --location{rc_location}

# cria o container registry
az acr create --resource-group nome_do_resourcegroup --name nome_do_acr --sku Basic

# Login to ACR
az acr login --name nome_do_acr

# Tag the image
docker tag landpage-projeto:latest nome_do_acr.azurecr.io/landpage-projeto:latest

# Push the image
docker push nome_do_acr.azurecr.io/landpage-projeto:latest




