import openxlab
openxlab.login(ak='vzranmjgawe4znm8wl56', sk='qmj6zq9dwxlyanennbvyo2p4wn5le3w1dv4gzavp', relogin=True)
from openxlab.model import upload
upload(model_repo='username/model_repo_name',
              file_type='metafile',
              source="/root/ft-oasst1/merged/metafile.yml")