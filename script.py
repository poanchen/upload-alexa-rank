import requests, csv, re
execfile("config.py")

# Download the sheets
print "Beginning to download the CSV from Google Sheets"
r = requests.get(config['excelDownloadUrl'])
open(config['excelFileName'], 'wb').write(r.content)
print "Finished downloading the sheets..."

# Convert CSV to JSON (Including Data Decimation)
import json
print "Converting CSV to JSON format..."
months = ['March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'January', 'February']
i = 0
json_data = []
been_throughed_months = set()
with open(config['excelFileName']) as csvDataFile:
  csvReader = csv.reader(csvDataFile)
  for row in csvReader:
    matchDate = re.match(r'^(%s) (\d*),\s(\d*)\sat\s\d\d:\d\d[AP]M' % months[i % 12], row[0])
    if matchDate and int(matchDate.group(2)) >= 10:
      date_and_time = matchDate.group(1) + ', ' + matchDate.group(3)
      if (date_and_time not in been_throughed_months and row[1] != '' and row[2] != '' and row[3] != '') or int(matchDate.group(2)) == 28:
        json_data.append({
          "Date and Time" : date_and_time,
          "Global Rank" : int(row[1]),
          "Top Ranked Country" : row[2] if row[2] != '' else "",
          "Country Rank" : int(row[3]) if row[3] != '' else "",
        })
        been_throughed_months.add(date_and_time)
        i = i + 1
print "Finished converting...Time to write to a file and save as JSON"
full_file_name = config['excelFileName'] +\
  "." +\
  config['excelFileExtension']
open(full_file_name, 'wb').write(json.dumps(json_data))
print "Finished writing."

# Upload the JSON file to my Azure Blob Storage
from azure.storage.blob import BlockBlobService
print "Beginning to upload the JSON file"
blob_service = BlockBlobService(config['accountName'], config['accountKey'])
full_path_to_file = config['excelFilePath'] +\
  full_file_name
blob_service.create_blob_from_path(
  config['containerName'],
  full_file_name,
  full_path_to_file)
print "Finished uploading the JSON file"
