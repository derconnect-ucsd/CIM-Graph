# Goal
* Get familiar with CIM-graph using our resources (schema and grid models).
* Test if grid models within "example grid models" can be read by CIM-graph using the schema file that was believed being used in OpenDSS at some point.

# Tips
* To convert an xsd file to a format used for the schema in cimgraph/data_profile/cimhub_2023.
1. Place the xsd schema file into the xsd sub directory
2. Run the terminal commands below
   
   'cd cimgraph/data_profile/'
   
   'xsdata generate ../../xsd/my_new_profile.xsd --package my_new_profile --config ../../xsd/config.xml'

3. Rename the import in the __init__.py file to read from cimgraph.data_profile.my_new_profile import (...

