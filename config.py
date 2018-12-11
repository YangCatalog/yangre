#  Author: Pieter Lewyllie, pilewyll@cisco.com
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  
#  http://www.apache.org/licenses/LICENSE-2.0
#  
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


import os
os.environ['LD_LIBRARY_PATH'] = "/usr/local/lib/:/usr/lib/x86_64-linux-gnu"

YANGGRE_PATH = "/usr/bin/yangre"
W3CGREP_PATH = "/home/yang/w3cgrep/w3cgrep"
PREFIX = "/yangre"  # changing this will break things, as it is also used in ajax calls
APIPREFIX = "/yangre/v1"
