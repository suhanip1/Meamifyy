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

# Function that will be called with dynamic paths
def process_conversion(selected_video, output_audio):
    convert_video_to_audio(selected_video, output_audio)

