[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/UxpU_KWG)

# ServerlessTemplate

How to Deploy:

1. Get the service_key needed to make changes in the Google Cloud Project (Can contact me e0550416@u.nus.edu)
1. Set path to service_key file as an environmental variable called `GOOGLE_APPLICATION_CREDENTIALS`
1. Install `npm`, `docker`, and `serverless` (https://www.serverless.com/framework/docs/providers/google/guide/installation)
1. Run `serverless deploy` to deploy the function to google cloud
1. Get the url returned by `serverless`