import xml.etree.ElementTree as ET
import string
import json
import os

def clean_line(line):
    clean_str, clean_line = "", []
    line = str(line).lower()
    for word in line:
        if not (word in string.punctuation or word in string.digits):
            clean_str += word
    clean_line = clean_str.split()
    return clean_line


def get_xml_data(path):
    tree = ET.parse(path) # Parse the XML file
    root = tree.getroot()

    # List to store text messages
    text_messages = []

    # Iterate over each 'text_message' element in the XML
    for text_message in root.findall('.//text_message'):
        message_body = text_message.find('message_body').text # Extract the message body
        cleaned_message = ' '.join(clean_line(message_body))
        text_messages.append(cleaned_message) # Add the message body to the list
    return text_messages

def write_to_file(path, text_list):
    with open(path, 'w', encoding='utf-8') as file:
        for item in text_list:
            file.write(item + '\n')


def get_json_data(path):
    with open(path) as file:
        messages = json.load(file)
    messages = data['smsCorpus']['message']

    # List to store text messages
    text_messages = []

    # Iterate over each text message in the json
    for message in messages:
        text_messages.append(' '.join(clean_line(str(message['text']['$']))))
    return text_messages


def get_json_data2(path):
    with open(path) as file:
        messages = json.load(file)

    # List to store text messages
    text_messages = []

    # Iterate over each text message in the json
    for message in messages:
        text_messages.append(' '.join(clean_line(str(message["lines"][0]["text"]))))
    return text_messages


def main():
    # Retrieving text messages from data\sources\Purdue_Calumet_text_Message_Corpus.xml, cleaning it and writing to file
    xml_path = 'data/sources/Purdue_Calumet_text_Message_Corpus.xml'
    file_path = 'data/cleaned_files/Purdue_Calumet_text_Message_Corpus.txt'
    if not os.path.exists(file_path):
        text = get_xml_data(xml_path)
        write_to_file(file_path, text)

    # Retrieving text messages from data\sources\smsCorpus_en.json, cleaning it and writing to file
    json_path = 'data/sources/smsCorpus_en.json'
    file_path = 'data/cleaned_files/smsCorpus_en.txt'
    if not os.path.exists(file_path):
        text = get_json_data(json_path)
        write_to_file(file_path, text)

    # Retrieving reddit conversations from data\sources\reddit_casual.json, cleaning it and writing to file
    json_path2 = 'data/sources/reddit_casual.json'
    file_path = 'data/cleaned_files/reddit_casual.txt'
    if not os.path.exists(file_path):
        text = get_json_data2(json_path2)
        write_to_file(file_path, text)


if __name__ == "__main__":
    main()
