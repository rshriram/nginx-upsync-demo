#!/bin/bash
echo "starting services"
docker-compose up -d
sleep 5
echo "setting upstream services"
helloworldv1=`docker inspect helloworld-v1|grep -w IPAddress|tail -1|cut -d : -f2|tr -d ' ",'`
helloworldv2=`docker inspect helloworld-v2|grep -w IPAddress|tail -1|cut -d : -f2|tr -d ' ",'`
hellotcpv1=`docker inspect hellotcp-v1|grep -w IPAddress|tail -1|cut -d : -f2|tr -d ' ",'`
hellotcpv2=`docker inspect hellotcp-v2|grep -w IPAddress|tail -1|cut -d : -f2|tr -d ' ",'`
echo "Registering services in Consul under /v1/kv/upstreams/"..
echo -n "registering helloworld-v1.."
curl -X PUT http://localhost:8500/v1/kv/upstreams/helloworld/${helloworldv1}:5000
echo ""
echo -n "registering helloworld-v2.."
curl -X PUT http://localhost:8500/v1/kv/upstreams/helloworld/${helloworldv2}:5000
echo ""
echo -n "registering hellotcp-v1.."
curl -X PUT http://localhost:8500/v1/kv/upstreams/hellotcp/${hellotcpv1}:5000
echo ""
echo -n "registering hellotcp-v2.."
curl -X PUT http://localhost:8500/v1/kv/upstreams/hellotcp/${hellotcpv2}:5000
echo ""

echo -e "You can now access http://localhost:8080/helloworld/hello for HTTP.\n For TCP, run ./client.py localhost 9080\nTo see list of upstreams in nginx, use curl http://localhost:8080/upstream_show (for http) and curl http://localhost:9180/upstream_show"
