import sys
import html
import os

def xml_to_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def txt_to_xml(text, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)
        
def check_file(xml_text):
    if '<a:title type="text">johndoe</a:title>' not in xml_text:
        return None
    if '<a:content type="html">BIOGRAPHY FIELD</a:content>' not in xml_text:
        return None
    return True

def encode_to_html(text_to_be_encoded):
    bio_text = html.escape(text_to_be_encoded)
    bio_text = bio_text.encode('ascii', 'xmlcharrefreplace').decode('ascii')
    bio_text = bio_text.replace('&#x27;', '&apos;')
    return bio_text

def update_bio_metadata(xml_text, artist_name, artist_bio):
    updated_text = xml_text.replace('<a:title type="text">johndoe</a:title>', f'<a:title type="text">{artist_name}</a:title>')
    updated_text = updated_text.replace('<a:content type="html">BIOGRAPHY FIELD</a:content>', f'<a:content type="html">{artist_bio}</a:content>')
    return updated_text

def change_name_folder(folder, artist):
    try:
        os.rename(folder, artist)
        print(f">>Folder renamed to '{artist}' and ready to make modifications.")
    except PermissionError:
        print(f">>Access denied to '{folder}'. Rename the folder manually.")
    except Exception as e:
        print(f">>Error trying to rename the folder: {e}")

def check_folder(folder):
    if os.path.exists(folder) and os.path.isdir(folder):
        print(f">>'{folder}' folder has been located.")
        return True
    else:
        return None

def artist_and_bio():
    print("Zune metadata artist folder assigner and bio editor - v0.5.3-beta")
    print('-'*65)
    try:
        folder = input("Enter the name of the folder to assign an artist: ")
        if not check_folder(folder):
            raise ValueError(f"'{folder}' folder not found.")
        bio_file = os.path.join(folder, 'Abyss Documents', 'htdocs', 'Zune HD Metadata Files', 'XML Documents', 'biography.xml')
        if not os.path.exists(bio_file):
            raise FileNotFoundError(f"This folder does not contain the 'biography.xml' file.")
        xml_text = xml_to_txt(bio_file)
        if not check_file(xml_text):
            raise ValueError("Maybe the 'biography.xml' file has been modified previously.")
        artist = input("Enter new artist name: ").strip()
        if not artist:
            raise ValueError("Artist's name cannot be empty.")
        biography = input('Enter artist bio: ').strip()
        if not biography:
            raise ValueError("Artist's bio cannot be empty.")
        bio_text = encode_to_html(biography)
        new_xml_text = update_bio_metadata(xml_text, artist, bio_text)
        txt_to_xml(new_xml_text, bio_file)
        print(">>Artist information successfully applied.")
        change_name_folder(folder, artist)
    
    except Exception as e:
        print(f"*Error: {e}")
        print(f'>Restart the program and try again.')
        os.system('pause')
        sys.exit(1)
    
    os.system('pause')
    
artist_and_bio()