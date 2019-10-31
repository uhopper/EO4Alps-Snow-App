# OGC

OGC services using MDI process API of DCFS project

## Development

### Setup
```
$ git clone https://github.com/eurodatacube/ogc-edc.git
$ cd ogc-edc

$ export SH_CLIENT_ID=<oauth_clientid>
$ export SH_CLIENT_SECRET=<oauth_clientsecret>
$ pip install requirements.txt
```

### Test
```
$ pytest --capture=no
```

### Run locally
```
$ env FLASK_APP=edc_ogc/app.py flask run
 * Serving Flask app "edc_ogc/app.py"
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

### Run with docker
`docker run -p 80:5000 -e SH_CLIENT_ID=<oauthclientid> -e SH_CLIENT_SECRET=<oauth_clientsecret> <image>`

### Try out
`http://localhost:5000/?service=WMS&version=1.1.0&request=GetMap&layers=AGRICULTURE&styles=&srs=EPSG:4326&bbox=14.043549,46.580095,14.167831,46.652688&width=512&height=512&format=image/png`
 
## Deployment

Travis-CI will automatically build and push docker image on checkin which will be pushed to docker hub.