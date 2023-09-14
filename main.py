import bibtexparser
from docx import Document


def format_author(author_str):
    author_formatted_str = ""
    authors_arr = author_str.split(" and ")
    count = 0
    for author in authors_arr:
        author_lastname = author.split(", ")[0]
        author_forname = author.split(", ")[1]
        if len(author_lastname) == 1:
            helper = author_lastname
            author_lastname = author_forname
            author_forname = helper
        author_forname_initial = author_forname[0]
        if count == 0:
            author_formatted_str = author_lastname + " " + author_forname_initial
            count = count + 1
        else:
            author_formatted_str = (
                author_formatted_str
                + ", "
                + author_lastname
                + " "
                + author_forname_initial
            )

    return author_formatted_str


def parseBibTexToString(file):
    library = bibtexparser.parse_file(file)

    formattedString = ""
    for el in library.entries:
        entry = el.fields_dict
        year = entry["year"].value
        author = format_author(entry["author"].value)
        title = entry["title"].value
        title = title.replace("{", "")
        title = title.replace("}", "")
        journal = entry["journal"].value
        pages = ""
        volume = ""
        try:
            volume = " " + entry["volume"].value + ": "
            pages = " " + entry["pages"].value
        except:
            print("Volume or pages not available")
        entryString = f"""{author} ({year}) {title}. {journal}{volume}{pages}."""

        if int(year) > 2021:
            formattedString = f"""
                {formattedString} <br/> <br/>
                {entryString}    
                """
    # print(formattedString)
    return formattedString


def parseBibTexToDocx(file):
    library = bibtexparser.parse_file(file)

    document = Document()

    document.add_heading("Citations", 0)

    for el in library.entries:
        entry = el.fields_dict
        author = format_author(entry["author"].value)
        year = entry["year"].value
        if int(year) < 2022:
            continue

        title = entry["title"].value
        title = title.replace("{", "")
        title = title.replace("}", "")
        journal = entry["journal"].value
        try:
            volume = entry["volume"].value
            pages = entry["pages"].value
        except:
            print("Volume or pages not available")

        p = document.add_paragraph("")
        p.add_run(author)
        p.add_run(" (" + year + ") " + title + ". ")
        p.add_run(journal).italic = True
        p.add_run(": " + pages + ".\n")
        c = document.add_paragraph("")

    document.save("citations.docx")
    return "document saved"
