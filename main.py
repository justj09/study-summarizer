from document_analyzer import analyze_documents
from document_loaders import CustomPDFLoader


if __name__ == "__main__":
    file_path = "ethics-textbook.pdf"
    start_page = 14
    end_page = 17

    loader = CustomPDFLoader(file_path)
    pages = []

    for i, page in enumerate(loader.lazy_load(), start=1):
        if i < start_page:
            continue
        if i > end_page:
            break
        pages.append(page)

    result = analyze_documents(pages)
    print("Description:", result.description, "\n")
    print("Summary:", result.summary)
