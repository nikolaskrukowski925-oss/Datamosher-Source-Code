import os
import struct
from pathlib import Path

def infinite_mosh():
    try:
        file_input = input("Drag AVI here: ").strip().replace('"', '').replace("'", "")
        if not os.path.exists(file_input):
            print("🚨 File not found.")
            return

        with open(file_input, 'rb') as f:
            data = bytearray(f.read())

        desktop = Path.home() / "Desktop"
        output_path = desktop / f"infinite_mosh_{os.path.basename(file_input)}"

        # Search for '00dc' video chunks
        target = b'00dc'
        pos = data.find(target)
        
        if_frame_count = 0
        moshed_count = 0
        
        while pos != -1:
            if pos + 8 < len(data):
                # Read the size of the chunk
                size = struct.unpack('<I', data[pos+4:pos+8])[0]
                
                # Logic: Large chunks are I-frames. 
                # We skip the 1st one so the video has a 'base' to start from.
                if size > 8000: # Threshold for I-frame detection
                    if_frame_count += 1
                    
                    if if_frame_count > 1:
                        # TARGET ACQUIRED: This is a subsequent I-frame.
                        # We overwrite it to prevent the 'reset' effect.
                        start_patch = pos + 8
                        end_patch = start_patch + size
                        
                        if end_patch < len(data):
                            # Overwrite with 0x00 to keep the smear rolling
                            data[start_patch:end_patch] = b'\x00' * size
                            moshed_count += 1
            
            # Find next chunk
            pos = data.find(target, pos + 4)

        with open(output_path, 'wb') as f:
            f.write(data)

        print("-" * 30)
        print(f"I-frames detected: {if_frame_count}")
        print(f"I-frames neutralized: {moshed_count}")
        print(f"The effect should now last until the end of the file.")
        print("-" * 30)

    except Exception as e:
        print(f"Error: {e}")
    
    input("\nPress ENTER to close...")

if __name__ == "__main__":
    infinite_mosh()