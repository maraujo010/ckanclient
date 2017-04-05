# ckanclient
python test: get info from ckan api with multiple asynchronous requests
  
- Fetches datasets using the CKAN API from http://beta.ckan.org and stores them in python data structures
- Calculates the amount of published datasets on http://beta.ckan.org
- Gives a total of external (not uploaded) vs internal (uploaded) resources on http://beta.ckan.org

File Description:
- ckanInfo.py (python script that runs the test)
- ckan.py     (python class module to fetch and process ckan data)

Install (module aiohttp):
``
pip3 install aiohttp
``
Run the script (the files must be executable):
``
./ckanInfo.py
``
