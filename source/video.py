from moviepy.editor import VideoFileClip


def process_video(input_file, output_file, function):
    clip = VideoFileClip(input_file)
    output_clip = clip.fl_image(function)
    output_clip.write_videofile(output_file, audio=False)
