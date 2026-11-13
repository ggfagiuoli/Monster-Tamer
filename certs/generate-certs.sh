#!/usr/bin/env bash
# Creates a private certificate authority (CA) and one HTTPS certificate per
# container, all signed by that CA. Every container trusts ca.crt, so services
# can check each other's certificates.
#
# Run from the repo root:   ./certs/generate-certs.sh
# Output goes to certs/out/ (ignored by git, never commit keys).
#
# Development only: these are self-signed, as the requirements ask.

set -euo pipefail

# TODO (guide step 2): add every new service here, using the same name as in
# docker-compose.yml. The name becomes the certificate's hostname.
SERVICES=(
  gateway
  monsters
  account
  historian
  encounter
  ownership
)

DAYS=365
OUT="$(cd "$(dirname "$0")" && pwd)/out"
mkdir -p "$OUT"
cd "$OUT"

# 1. The CA: made once, reused on later runs so existing certs stay valid.
if [[ ! -f ca.key ]]; then
  echo "Creating CA"
  openssl genrsa -out ca.key 4096 2>/dev/null
  # The extensions mark it as a real CA. Strict TLS clients (Python 3.13+)
  # reject a CA certificate without them.
  openssl req -x509 -new -key ca.key -sha256 -days "$DAYS" \
    -subj "/CN=Monster Tamers dev CA" \
    -addext "basicConstraints=critical,CA:TRUE,pathlen:0" \
    -addext "keyUsage=critical,keyCertSign,cRLSign" \
    -addext "subjectKeyIdentifier=hash" \
    -out ca.crt
fi

# 2. One key + certificate per service.
for name in "${SERVICES[@]}"; do
  echo "Creating certificate for $name"
  openssl genrsa -out "$name.key" 2048 2>/dev/null
  openssl req -new -key "$name.key" -subj "/CN=$name" -out "$name.csr"

  # The certificate is valid for the docker hostname and for localhost
  # (localhost is used by the healthchecks and by the frontend for the gateway).
  cat > "$name.ext" <<EOF
basicConstraints=critical,CA:FALSE
keyUsage=critical,digitalSignature,keyEncipherment
extendedKeyUsage=serverAuth
subjectAltName=DNS:$name,DNS:localhost,IP:127.0.0.1
subjectKeyIdentifier=hash
authorityKeyIdentifier=keyid,issuer
EOF

  openssl x509 -req -in "$name.csr" -CA ca.crt -CAkey ca.key -CAcreateserial \
    -days "$DAYS" -sha256 -extfile "$name.ext" -out "$name.crt" 2>/dev/null
  rm -f "$name.csr" "$name.ext"
done

# Containers run as non-root users with a different user id than yours, so they
# need read access to their key. Acceptable for local self-signed dev certs only.
chmod 644 ./*.key ./*.crt
chmod 600 ca.key

echo "Done. Files are in certs/out/"
