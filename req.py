import requests



me = { \
"latitude":"52.164312",\
"longitude":"-115.164312",\
"type":"phosphate",\
"reference_measurements":[ 215, 42, 108, 224, 96, 144, 215, 121, 147, 214, 135, 154,211, 166, 161, 205, 185, 178, 209, 185, 161 ],\
"measurement":[ 214,181,176, 214,181,176, 214,181,176, 214,181,176 ,214,181,176,214,181,176, 214,181,176, 214,181,176, 214,181,176 ],\
"color_correction":"1.25",\
"color_method":1,\
"mass_concentration":3.12,\
"light_condition":5,\
"at_sampling_location":True,\
"origin_of_water":"WetLand",\
"temperature":"​29.3",\
"mass_concentration_uncorrected": 3.12,\
"error_message": "Calculation completed successfully",\
"label": "label",\
"reference_concentrations": [50, 20, 10, 5, 2, 1, 0, 1]\
}
#print(data)
#r = requests.post("https://gwf-nutrient.usask.ca/api/v1/samples/collect_data", json=me)
r = requests.post("http://localhost:5000/api/v1/samples/collect_data", json=me)
print(r.content)
print(r)
#"temperature":"​29.3"
#"latitude":"52.164312",\
#"color_method":1,\
