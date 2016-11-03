FROM rshriram/nginx-1.11.5-upsync-modules
ENTRYPOINT [ "/opt/run_nginx.sh" ]
EXPOSE 8080 9080 9180
