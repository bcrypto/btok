#!/bin/bash
# =============================================================================
# \brief Issuing model CV-certificates
# \project btok/model
# \created 2025.01.15
# \version 2025.01.16
# \pre Bee2cmd (https://github.com/agievich/bee2) is installed.
# =============================================================================

bee2cmd="${BEE2CMD:-./bee2cmd}"
if [ ! -f "${bee2cmd}" ]; then
  bee2cmd=$(command -v bee2cmd)
  if [ ! -f "${bee2cmd}" ]; then
    echo "Set path to bee2cmd executable file to BEE2CMD environment \
      variable or run this script from containing folder."
    exit 1
  fi
fi
this=$(realpath $BASH_SOURCE)

# =============================================================================
# Entities:
# * ca0 --- root CA (zed);
# * ca1 --- subordinate CA (trent);
# * term --- terminal (terence);
# * ct --- token (alice).
#
# Objects:
# * .sk --- private key;
# * .cert --- certificate;
# * .link --- link certificate.

# Certificates:
#   ca0000.cert (root) ---- ca0001.link
#    |  |                   ca0001.cert (new root)
#    |  + ----- ca1000.cert
#    |             |
# ct.cert       term.cert
# =============================================================================

# ca0: setup

$bee2cmd kg gen -l128 -pass pass:zed ca0000.sk

$bee2cmd cvc root -authority BYCA0000 \
  -from 250115 -until 300114 \
  -eid 3F3FFFFF33 -esign F7E0 \
  -pass pass:zed ca0000.sk ca0000.cert

# ca1: enroll

$bee2cmd kg gen -l128 -pass pass:trent ca1000.sk

$bee2cmd cvc req -authority BYCA0000 -holder BYCA1000 \
  -from 250201 -until 250731 \
  -eid 3F3FFFFF33 -esign F7E0 \
  -pass pass:trent ca1000.sk ca1000.req

$bee2cmd cvc iss -pass pass:zed ca0000.sk ca0000.cert \
  ca1000.req ca1000.cert

rm -f ca1000.req

# term: enroll

$bee2cmd kg gen -l128 -pass pass:terence term.sk

$bee2cmd cvc req -authority BYCA1000 -holder 001123456789 \
  -from 250701 -until 250703 \
  -eid 003C6F5B10 -esign F200 \
  -pass pass:terence term.sk term.req

$bee2cmd cvc iss -pass pass:trent ca1000.sk ca1000.cert \
  term.req term.cert

rm -f term.req

# ct: enroll

$bee2cmd kg gen -l128 -pass pass:alice ct.sk

$bee2cmd cvc req -authority BYCA0000 -holder 000123456789 \
  -from 250322 -until 350321 \
  -pass pass:alice ct.sk ct.req

$bee2cmd cvc iss -pass pass:zed ca0000.sk ca0000.cert \
  ct.req ct.cert

rm -f ct.req

# ca0: update

$bee2cmd kg gen -l128 -pass pass:zed ca0001.sk

$bee2cmd cvc root -authority BYCA0001 -holder BYCA0001 \
  -from 300101 -until 341231 \
  -eid 3F3FFFFF33 -esign F7E0 \
  -pass pass:zed ca0001.sk ca0001.req

$bee2cmd cvc req -authority BYCA0000 -holder BYCA0001 \
  -from 300101 -until 341231 \
  -eid 3F3FFFFF33 -esign F7E0 \
  -pass pass:zed ca0001.sk ca0001.req

$bee2cmd cvc iss -pass pass:zed ca0000.sk ca0000.cert \
  ca0001.req ca0001.cert

rm -f ca0001.req
