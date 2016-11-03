# nginx-upsync-demo
This repository contains a compiled version of nginx 1.11.5 with the [http upsync module](https://github.com/weibocom/nginx-upsync-module) and the [stream upsync module](https://github.com/xiaokai-wang/nginx-stream-upsync-module) that is capable of updating the upstreams dynamically from Consul.

## Requirements

* Docker Compose
* Python 2.7

## Usage

```bash
./run_services.sh
```

This should start a simple setup with a nginx gateway and two backend microservices _helloworld_ (a HTTP service) and _hellotcp_ (a TCP service) each with two upstream instances. Each instance represents a different version of the same backend service.

You can now access http://localhost:8080/helloworld/hello for the _helloworld_ HTTP microservice. The output would alterntate between two versions of the helloworld (v1 and v2).

```bash
curl http://localhost:8080/helloworld/hello
```

To access the _hellotcp_ TCP based microservice, run `./client.py localhost 9080`. The output would alternate between two versions of the hellotcp service (v1 and v2).

```bash
./client.py localhost 9080
```

To see list of upstreams in nginx,

```bash
#for HTTP services
curl http://localhost:8080/upstream_show
#for TCP services
curl http://localhost:9180/upstream_show
```

### Changing the weights

In order to increase the weights for a particular version of the service (e.g., helloworld v2),

* Get the IP address of helloworld-v2 service using the following command

```bash
helloworldv2=`docker inspect helloworld-v2|grep -w IPAddress|tail -1|cut -d : -f2|tr -d ' ",'`
```

* Update Consul's entry for helloworld-v2 with appropriate weights (this gets translated into nginx's weights for upstream instances automatically).

```bash
curl -X PUT -d "{\"weight\":3, \"max_fails\":2, \"fail_timeout\":10}" http://localhost:8500/v1/kv/helloworld/${helloworldv2}:5000
```

* Access helloworld

```bash
curl http://localhost:8080/helloworld/hello
```

You should see the traffic being split into 25% for helloworld v1 and 75% for helloworld v2.
