# Why?

I wanted a dead simple way to share information with the web server about containers running one-off commands without exposing the docker socket to them. 

### Build the image

```docker image build -t detlbr .```

### Run it
```docker run  -v /var/run/docker.sock:/var/run/docker.sock -e CURRENT_PROJECT=myproject -p 8000:8000  -ti detlbr```



