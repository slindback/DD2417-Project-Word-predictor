def concatenate_files():
    input_files = ['Purdue_Calumet_text_Message_Corpus.txt', 'reddit_casual.txt', 'smsCorpus_en.txt']
    output_file = 'all_concat.txt'

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for file_name in input_files:
            with open(file_name, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())

    print("Files concatenated successfully!")

if __name__ == "__main__":
    concatenate_files()
