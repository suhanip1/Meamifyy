from moviepy.editor import VideoFileClip

def convert_video_to_audio(video_path, audio_path):
    # Load the video file
    video_clip = VideoFileClip(video_path)
    
    # Extract the audio
    audio_clip = video_clip.audio
    
    # Write the audio to a file
    audio_clip.write_audiofile(audio_path)
    
    # Close the clips
    audio_clip.close()
    video_clip.close()

# Path to your video file
video_path = "/Users/kabir/Desktop/IgnitionHacks/SuhaniMain/Meamifyy/material/Probability Grade 10 _ Introduction.mp4"

# Path where you want to save the audio file with filename and extension
audio_path = "/Users/kabir/Desktop/IgnitionHacks/SuhaniMain/Meamifyy/material/audio_output.mp3"

# Convert video to audio
convert_video_to_audio(video_path, audio_path)

print("Conversion completed! Audio saved at:", audio_path)
