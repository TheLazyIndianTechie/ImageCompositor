from PIL import Image
import io

# Removed redundant imports and ensured only the necessary ones are used.

# Define a function to open images to reduce repetition
def open_image(image_path):
    try:
        return Image.open(image_path)
    except IOError as e:
        print(f"Unable to open image {image_path}: {e}")
        exit(1)

background_path = 'composite-scenic-background.jpg'
male_character_path = 'rpm-ai-test-male.png'
female_character_path = 'rpm-ai-test-female.png'

print("Opening images...")
background = open_image(background_path)
male_character = open_image(male_character_path)
female_character = open_image(female_character_path)

# Encapsulate the resizing logic into a function
def resize_avatar(avatar, scale_multiplier):
    return avatar.resize((avatar.width * scale_multiplier, avatar.height * scale_multiplier))

try:
    # Get user input for avatar scale multiplier and convert it to an integer
    avatar_scale_multiplier = int(input("Enter avatar scale multiplier: "))
except ValueError:
    print("Invalid input for avatar scale multiplier. Please enter an integer.")
    exit(1)

print("Resizing avatars...")
male_character = resize_avatar(male_character, avatar_scale_multiplier)
female_character = resize_avatar(female_character, avatar_scale_multiplier)

print("Calculating positions...")
male_position = ((background.width - male_character.width) // 2, background.height - male_character.height)
female_position = (male_position[0] + male_character.width, background.height - female_character.height)

print("Pasting male character...")
background.paste(male_character, male_position, male_character)

print("Pasting female character...")
background.paste(female_character, female_position, female_character)

def save_image_with_progress(image, filename):
    """
    Save the image to a file with a progress bar reflecting the actual write progress.
    """
    # Define a subclass of BytesIO to override the write method and update the progress bar
    class ProgressBytesIO(io.BytesIO):
        def __init__(self, total_size):
            super().__init__()
            self.total_size = total_size
            self.bytes_written = 0
        
        def write(self, b):
            # Update the progress bar with the number of bytes written
            self.bytes_written += len(b)
            print(f"Saving progress: {self.bytes_written / self.total_size * 100:.2f}%", end='\r')
            return super().write(b)

    # Get the estimated size of the image in bytes
    estimated_size = len(image.tobytes())
    # Create a ProgressBytesIO instance
    output_stream = ProgressBytesIO(estimated_size)
    # Save the image using the custom BytesIO subclass
    image.save(output_stream, format='PNG')
    # Get the contents of the BytesIO object and write it to the actual file
    with open(filename, 'wb') as f:
        f.write(output_stream.getvalue())

    print("\nImage saved successfully.")

filename = input("Enter filename for the final image (with .png extension): ")
if not filename.endswith('.png'):
    print("Invalid filename. Please make sure the filename ends with .png extension.")
    exit(1)

# Call the function to save the image with progress
save_image_with_progress(background, filename)

print("Done.")

