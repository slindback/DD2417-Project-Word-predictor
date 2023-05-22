def remove_adjacent_duplicates(file_path):
    with open(file_path, 'r', encoding='utf8') as file:
        lines = file.readlines()

    cleaned_lines = []
    prev_line = None
    dups = 0

    for line in lines:
        if line != prev_line:
            cleaned_lines.append(line)
        else:
            dups += 1
        prev_line = line

    with open(file_path, 'w', encoding='utf8') as file:
        file.writelines(cleaned_lines)

    print("{} duplicates removed successfully!".format(dups))

if __name__ == "__main__":
    file_paths = ['Purdue_Calumet_text_Message_Corpus.txt', 'reddit_casual.txt', 'smsCorpus_en.txt']
    for file in file_paths:
        remove_adjacent_duplicates(file)
