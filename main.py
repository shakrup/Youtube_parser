import json
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

# API key
api_key = "your API is here"

# Create a YouTube service object
try:
    youtube = build("youtube", "v3", developerKey=api_key)
except HttpError as error:
    print(f"An HTTP error occurred: {error}")
    exit()

# Create a search request
try:
    request = youtube.search().list(
        part="snippet",
        type="video",
        maxResults=121,
        # paste your location in longitude and latitude format
        location="-12.152, 96.870",
        locationRadius="500km",
        order="viewCount"
    )
    # Execute the request
    response = request.execute()
except HttpError as error:
    print(f"An error occurred while making the request: {error}")
    exit()

# Extract the video data
video_data = response.get("items", [])
if not video_data:
    print("No video data found.")
    exit()

# Create a list to store the video information
video_list = {"videos": []}

# Iterate through the video data
for video in video_data:
    # Extract the video title, channel title, and video URL
    title = video["snippet"]["title"]
    channel_title = video["snippet"]["channelTitle"]
    published_at = video["snippet"]["publishedAt"]
    video_url = "https://www.youtube.com/watch?v=" + video["id"]["videoId"]

    # Append the video information to the list
    video_list["videos"].append({"title":title, "channel_title": channel_title, "publishedAt":published_at, "video_url":video_url,"time": published_at})
    # Sorting by time
    video_list["videos"] = sorted(video_list["videos"], key=lambda k: k['time'])

# Dump the video_list to json
try:
    with open("youtube.json", "w", encoding='utf-8') as outfile:
        json.dump(video_list, outfile, indent=4, ensure_ascii=False)
except Exception as e:
    print(f"An error occurred while writing to youtube.json: {e}")


