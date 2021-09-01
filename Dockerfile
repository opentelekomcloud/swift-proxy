# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM docker.io/opendevorg/python-builder:3.9 as builder
ENV DEBIAN_FRONTEND=noninteractive

ARG ZUUL_SIBLINGS=""
COPY . /tmp/src
RUN echo "gunicorn" >> /tmp/src/requirements.txt
RUN assemble

FROM docker.io/opendevorg/python-base:3.9 as swift-proxy
ENV DEBIAN_FRONTEND=noninteractive

COPY --from=builder /output/ /output
RUN mkdir /etc/swift-proxy

RUN /output/install-from-bindep \
  && rm -rf /output \
  && useradd -u 10001 -m -d /var/lib/swift_proxy -c "Swift Proxy" swift_proxy \
  && chown -R 10001 /etc/swift-proxy

VOLUME /var/lib/swift_proxy

USER 10001
CMD ["gunicorn", "-b 0.0.0.0:8000", \
#    # 4 workers
     "-w 4", \
     "--access-logfile", "-", \
     "swift_proxy.app:app"]

