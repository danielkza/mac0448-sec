#!/bin/sh

set -e

mkdir -p certs
cd certs

openssl req -new -x509 -extensions v3_ca -keyout ca_key.pem -out ca_cert.pem \
 -nodes -subj "/CN=$(hostname -f)/O=EP2 CA/C=BR"
openssl req -newkey rsa:2048 -keyout server_key.pem -out server_cert.csr -nodes \
 -subj "/CN=$(hostname -f)/O=EP2/C=BR"
openssl x509 -req -in server_cert.csr -out server_cert.pem -CA ca_cert.pem \
 -CAkey ca_key.pem -CAcreateserial
