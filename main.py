import os
import glob
from PyPDF2 import PdfMerger


def compress_pdf(pdf_path: str, outputpath: str):
    filename = os.path.splitext(os.path.basename(pdf_path))[0]

    outputfile = os.path.join(outputpath, f"{filename}_compressed.pdf")
    os.system(
        f"gswin64c -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 \
                -dPDFSETTINGS=/screen -dNOPAUSE -dBATCH \
                -sOutputFile={outputfile} {pdf_path}"
    )


def compress_folder(in_path: str, out_path: str):
    if not os.path.exists(out_path):
        os.mkdir(out_path)

    items = os.listdir(out_path)

    if len(items) > 0:
        for item in items:
            os.remove(os.path.join(out_path, item))

    pdf_files = glob.glob(os.path.join(in_path, "*.pdf"))
    for pdf_file in pdf_files:
        compress_pdf(pdf_file, out_path)


def merge_folder(in_path: str, out_name: str, out_path: str = "./merged"):
    if not os.path.exists(out_path):
        os.mkdir(out_path)

    files = [os.path.join(in_path, filename) for filename in os.listdir(in_path)]

    if len(files) == 0:
        print("no pdf found to join")
        return

    with PdfMerger() as merger:
        for pdf in files:
            merger.append(pdf)

        out_file = os.path.join(out_path, out_name)

        merger.write(out_file)


if __name__ == "__main__":
    in_path = "./pdfin/"
    path_compressed = "./compressed/"
    merged_name = "test.pdf"

    compress_folder(in_path, path_compressed)
    merge_folder(path_compressed, merged_name)
