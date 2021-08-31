===========
Swift Proxy
===========


Sometimes you just need to serve content stored in OpenStack Swift requiring
some form of Authorization which Swift itself does not support (i.e. basic
auth). This project solves this problem by providing a tiny Flask based WSGI
application that can be deployed in the web server implementing any required
authorization.

As the configuration the project requires following:
- `SITE_NAME` - Prefix of the swift where requests would be redirected to (eg.
  `SITE_NAME=https://my.swift/v1/AUTH_FAKE` will result in request
  http://localhost:8000/a/b/c to be served from
  https://my.swift/v1/AUTH_FAKE/a/b/c
* `CLOUD_NAME` - Name of the cloud from clouds.yaml
