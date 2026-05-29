from moviepy import VideoFileClip, concatenate_videoclips
import os, sys

def cut_and_compile_video(input_path, output_path, cut_intervals):
    """
    Cuts specific chunks from a video and compiles them into a new video.

    Args:
        input_path (str): Path to the input video file.
        output_path (str): Path to save the final compiled video.
        cut_intervals (list of tuples): List of (start_time, end_time) in seconds.
    """
    if not os.path.exists(input_path):
        print(f"Error: Input video '{input_path}' not found.")
        return

    try:
        # Load the original video
        print(f"Loading video: {input_path}")
        video = VideoFileClip(input_path)

        clips = []
        # Extract each chunk based on the provided intervals
        for start, end in cut_intervals:
            print(f"Extracting clip from {start}s to {end}s...")
            # Create a subclip using start and end times in seconds
            clip = video.subclipped(start, end)
            clips.append(clip)

        # Concatenate all extracted chunks in the order they appear in the list
        print("Concatenating clips...")
        final_video = concatenate_videoclips(clips)

        # Write the final video to a file
        # Using libx264 and aac ensures broad compatibility (like standard MP4s)
        print(f"Writing final video to {output_path}...")
        final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

        # Close the clips to free up system memory
        video.close()
        for clip in clips:
            clip.close()
        final_video.close()

        print("\nSuccess! Video cut and compiled successfully.")

    except Exception as e:
        print(f"\nAn error occurred during processing: {e}")


# ==========================================
# Script Execution / Example Usage
# ==========================================
import time
if __name__ == "__main__":
    # 1. Define your input and output file paths
    input_video = sys.argv[1] 
    output_video = "salus_demo.mp4" # Replace with your desired output filename
    t0=time.time()
    print(f'FROM: {input_video} TO: {output_video}')

    # 2. Define the chunks you want to keep
    # Format: A list of tuples containing (start_time_in_seconds, end_time_in_seconds)
    # You can use integers or floats (e.g., 10.5 for 10 and a half seconds)
    intervals = [
        (4, 9),          # intro
	(36, 41),        # resumen historico
	(100,110),        # transcripcion
	(120,125),        # resumen transcripcion
	(180,190),        # propuesta ficha
]

    # 3. Run the compiler
    cut_and_compile_video(input_video, output_video, intervals)
    tf=time.time()
    print('-'*32);print('DT:', round(tf-t0,2),'secs')