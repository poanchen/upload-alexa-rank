# upload-alexa-rank
Keep poanchen.github.io/alexa-rank updated once a month.

## Why is this useful?
We need to keep poanchen.github.io/alexa-rank updated once a month. There will be a lot of manual works involved, for example, manually going through the long Google Sheets, picking out rows from the sheet, paste it somewhere else like a JSON, keep doing that until everything is covered, then simply upload the file to Azure Blob Storage. And, of course, we need to do this at least once a month. With automation, all these can be done once and for all. How does that sound?

## Getting started

### Prerequisites:
- Python 2.7 or up
- A remote web server that allows you to run a cron job

### Installation
To begin, make sure you already have a Google Sheet that store your Alexa ranks. If you have not done so, go [here](https://github.com/poanchen/add-alexa-rank-ifttt). Clone this guy.

### Development environment
Tested on Ubuntu 14.04.X LTS server but theoretically it should work on OS X as well.

### Usage
You want to change the config file to match your own settings,
```
config = {}

config['excelDownloadUrl'] = "urlToYourGoogleSheet"
config['excelFileName'] = "yourFileName"
config['excelFileExtension'] = "json"
config['excelFilePath'] = "absolutePathToYourScript"

# Azure Portal
config['accountName'] = "azureAccountName"
config['accountKey'] = "azureAccountKey"

# Azure Blob Storage
config['containerName'] = "containerName"
```
In case you do not know what your account name, account key, or even container name, check out [this](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python#copy-your-credentials-from-the-azure-portal) tutorial by [Microsoft](https://docs.microsoft.com). Please make sure not to commit your azure account key to public site like GitHub.com. Use environment variable to make it a secret while keeping the code on GitHub. If you need help on this, check out [this](https://github.com/poanchen/add-alexa-rank-ifttt#usage).

Now, all you need to do is to hook this script up with a cron job and you are done.

This is how I set up my cron job.
```
00 9 15 * * cd /path/to/the/upload-alexa-rank; python script.py >> output.log;  date >> output.log;
```
This cron job will run the script once a month at 9am sharp on the 15th of the calendar month. It will also record any log to the output.log for debugging purposes.
