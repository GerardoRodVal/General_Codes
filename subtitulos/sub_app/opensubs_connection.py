from opensubtitlescom import OpenSubtitles
import json

subtitles = OpenSubtitles("MyApp v1.0.0", "SDI6uXyLXr80HhFIuYoIrNFXph1Or6cl")
subtitles.login('_galighieri_', 'Visorak1!')

response = subtitles.search(query="Hellraiser", languages="es")

r_json = response.to_json()
json_str = r_json.rstrip(',')
list_json = json.loads(json_str)
print(list_json)
names_sub = {}
for id,movie_i in enumerate(list_json['data']):
    print(movie_i)
    print(movie_i['file_name'])
    name = movie_i['file_name']
    print('-'*50)
    names_sub[name] = id
#print(response.data[0])
srt = subtitles.download_and_parse(response.data[0])
#print(srt)