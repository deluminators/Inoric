!pip install awscli
import boto3
# Let's use Amazon S3
s3 = boto3.resource('s3') 

import boto3

# Create a low-level client with the service 
sqs = boto3.client('sqs')

# Import everything needed to edit video clips
from moviepy.editor import *

# Load myHolidays.mp4 and select the subclip 00:00:50 - 00:00:60
clip = VideoFileClip("myHolidays.mp4").subclip(50,60)

# Reduce the audio volume (volume x 0.8)
clip = clip.volumex(0.8)

# Generate a text clip. You can customize the font, color, etc.
txt_clip = TextClip("My Holidays 2013",fontsize=70,color='white')

# Say that you want it to appear 10s at the center of the screen
txt_clip = txt_clip.set_pos('center').set_duration(10)

# Overlay the text clip on the first video 
clipvideo = CompositeVideoClip([clip, txt_clip])

# Write the result to a file (many options available !)
video.write_videofile("myHolidays_edited.webm")

# Create Transcription Job
response = createTranscribeJob( args.region, args.inbucket, args.infile )

# loop until the job successfully completes
print( "\n==> Transcription Job: " + response["TranscriptionJob"]["TranscriptionJobName"] + "\n\tIn Progress"),

while( response["TranscriptionJob"]["TranscriptionJobStatus"] == "IN_PROGRESS"):
    print( "."),
    time.sleep( 30 )
    response = getTranscriptionJobStatus( response["TranscriptionJob"]["TranscriptionJobName"] )

print( "\nJob Complete")
print( "\tStart Time: " + str(response["TranscriptionJob"]["CreationTime"]) )
print( "\tEnd Time: "  + str(response["TranscriptionJob"]["CompletionTime"]) )
print( "\tTranscript URI: " + str(response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]) )

# Now get the transcript JSON from AWS Transcribe
transcript = getTranscript( str(response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]) ) 
# print( "\n==> Transcript: \n" + transcript)


import boto3
import uuid
import requests

# purpose: Function to format the input parameters and invoke the Transcribe service
def createTranscribeJob( region, bucket, mediaFile ):

    # Set up the Transcribe client 
    transcribe = boto3.client('transcribe')
    
    # Set up the full uri for the bucket and media file
    mediaUri = "https://" + "s3-" + region + ".amazonaws.com/" + bucket + mediaFile 
    
    print( "Creating Job: " + "transcribe" + mediaFile + " for " + mediaUri )
    
    # Use the uuid functionality to generate a unique job name.  Otherwise, the Transcribe service will return an error
    response = transcribe.start_transcription_job( TranscriptionJobName="transcribe_" + uuid.uuid4().hex + "_" + mediaFile , \
        LanguageCode = "en-US", \
        MediaFormat = "mp4", \
        Media = { "MediaFileUri" : mediaUri }, \
        Settings = { "VocabularyName" : "MyVocabulary" } \
        )
    
    # return the response structure found in the Transcribe Documentation
    return response
    
    
# purpose: simply return the job status    
def getTranscriptionJobStatus( jobName ):
    transcribe = boto3.client('transcribe')
    
    response = transcribe.get_transcription_job( TranscriptionJobName=jobName )
    return response
    
# purpose: get and return the transcript structure given the provided uri
def getTranscript( transcriptURI ):
    # Get the resulting Transcription Job and store the JSON response in transcript
    result = requests.get( transcriptURI )

    return result.text
    
..

translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)

...

def translateTranscript( transcript, sourceLangCode, targetLangCode ):
    # Get the translation in the target language.  We want to do this first so that the translation is in the full context
    # of what is said vs. 1 phrase at a time.  This really matters in some lanaguages

    # stringify the transcript
    ts = json.loads( transcript )

    # pull out the transcript text and put it in the txt variable
    txt = ts["results"]["transcripts"][0]["transcript"]
        
    # call Translate  with the text, source language code, and target language code.  The result is a JSON structure containing the 
    # translated text
    translation = translate.translate_text(Text=txt,SourceLanguageCode=sourceLangCode, TargetLanguageCode=targetLangCode)
    
    return translation
    
    
def getPhrasesFromTranscript( transcript ):

    # This function is intended to be called with the JSON structure output from the Transcribe service.  However,
    # if you only have the translation of the transcript, then you should call getPhrasesFromTranslation instead

    # Now create phrases from the translation
    ts = json.loads( transcript )
    items = ts['results']['items']
    
    #set up some variables for the first pass
    phrase =  newPhrase()
    phrases = []
    nPhrase = True
    x = 0
    c = 0

    print "==> Creating phrases from transcript..."

    for item in items:

        # if it is a new phrase, then get the start_time of the first item
        if nPhrase == True:
            if item["type"] == "pronunciation":
                phrase["start_time"] = getTimeCode( float(item["start_time"]) )
                nPhrase = False
            c+= 1
        else:    
            # We need to determine if this pronunciation or puncuation here
            # Punctuation doesn't contain timing information, so we'll want
            # to set the end_time to whatever the last word in the phrase is.
            # Since we are reading through each word sequentially, we'll set 
            # the end_time if it is a word
            if item["type"] == "pronunciation":
                phrase["end_time"] = getTimeCode( float(item["end_time"]) )
                
        # in either case, append the word to the phrase...
        phrase["words"].append(item['alternatives'][0]["content"])
        x += 1
        
        # now add the phrase to the phrases, generate a new phrase, etc.
        if x == 10:
            #print c, phrase
            phrases.append(phrase)
            phrase = newPhrase()
            nPhrase = True
            x = 0
            
    return phrases    
def getTimeCode( seconds ):
# Format and return a string that contains the converted number of seconds into SRT format

   thund = int(seconds % 1 * 1000)
    tseconds = int( seconds )
   tsecs = ((float( tseconds) / 60) % 1) * 60
   tmins = int( tseconds / 60 )
   return str( "%02d:%02d:%02d,%03d" % (00, tmins, int(tsecs), t_hund ))
    
def getPhrasesFromTranslation( translation, targetLangCode ):

    # Now create phrases from the translation
    words = translation.split()
    
    #set up some variables for the first pass
    phrase =  newPhrase()
    phrases = []
    nPhrase = True
    x = 0
    c = 0
    seconds = 0

    print "==> Creating phrases from translation..."

    for word in words:

        # if it is a new phrase, then get the start_time of the first item
        if nPhrase == True:
            phrase["start_time"] = getTimeCode( seconds )
            nPhrase = False
            c += 1
                
        # Append the word to the phrase...
        phrase["words"].append(word)
        x += 1
        
        
        # now add the phrase to the phrases, generate a new phrase, etc.
        if x == 10:
        
            # For Translations, we now need to calculate the end time for the phrase
            psecs = getSecondsFromTranslation( getPhraseText( phrase), targetLangCode, "phraseAudio" + str(c) + ".mp3" ) 
            seconds += psecs
            phrase["end_time"] = getTimeCode( seconds )
        
            phrases.append(phrase)
            phrase = newPhrase()
            nPhrase = True

            x = 0
            
    return phrases
    
    
def getSecondsFromTranslation( textToTranslate, targetLangCode, audioFileName ):

    # Set up the Amazon Polly and Amazon Translate services
    client = boto3.client('polly')
    translate = boto3.client(service_name='translate', region_name="us-east-1", use_ssl=True)
    
    # Use the translated text to create the synthesized speech
    response = client.synthesize_speech( OutputFormat="mp3", SampleRate="22050", Text=textToTranslate, VoiceId=getVoiceId( targetLangCode ) )
    
    # Write the stream out to disk so that we can load it into an AudioClip
    writeAudioStream( response, audioFileName )
    
    # Load the temporary audio clip into an AudioFileClip
    audio = AudioFileClip( audioFileName)
        
    # return the duration    
    return audio.duration
    

    # Use the translated text to create the synthesized speech
    response = client.synthesize_speech( OutputFormat="mp3", SampleRate="22050", Text=translated_txt, VoiceId=voiceId)
    
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        print( "\t==> Successfully called Polly for speech synthesis")
        writeAudioStream( response, audioFileName )
    else:
        print( "\t==> Error calling Polly for speech synthesis")
    
...


def writeAudioStream( response, audioFileName ):
    
    # Take the resulting stream and write it to an mp3 file
    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            output = audioFileName
            writeAudio( output, stream )    
