import os
from typing import List, Tuple

import pymupdf


class PDFFileLoader:
    def __init__(self, path: str):
        self.documents = []  # List of (text, filename) tuples
        self.path = path

    def load(self):
        if os.path.isdir(self.path):
            self.load_directory()
        elif os.path.isfile(self.path) and self.path.endswith(".pdf"):
            self.load_file()
        else:
            raise ValueError(
                "Provided path is neither a valid directory nor a .pdf file."
            )

    def load_file(self):
        doc = pymupdf.open(self.path)
        text = ""
        for page in doc:
            text += page.get_text()
        filename = os.path.basename(self.path)
        self.documents.append((text, filename))

    def load_directory(self):
        for root, _, files in os.walk(self.path):
            for file in files:
                if file.endswith(".pdf"):
                    doc = pymupdf.open(os.path.join(root, file))
                    text = ""
                    for page in doc:
                        text += page.get_text()
                    self.documents.append((text, file))

    def load_documents(self) -> List[Tuple[str, str]]:
        self.load()
        return self.documents


class TextFileLoader:
    def __init__(self, path: str, encoding: str = "utf-8"):
        self.documents = []
        self.path = path
        self.encoding = encoding

    def load(self):
        if os.path.isdir(self.path):
            self.load_directory()
        elif os.path.isfile(self.path) and self.path.endswith(".txt"):
            self.load_file()
        else:
            raise ValueError(
                "Provided path is neither a valid directory nor a .txt file."
            )

    def load_file(self):
        with open(self.path, "r", encoding=self.encoding) as f:
            self.documents.append(f.read())

    def load_directory(self):
        for root, _, files in os.walk(self.path):
            for file in files:
                if file.endswith(".txt"):
                    with open(
                        os.path.join(root, file), "r", encoding=self.encoding
                    ) as f:
                        self.documents.append(f.read())

    def load_documents(self):
        self.load()
        return self.documents


class CharacterTextSplitter:
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        split_mode: str = "character",
    ):
        assert (
            chunk_size > chunk_overlap
        ), "Chunk size must be greater than chunk overlap"

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.split_mode = split_mode

    def split(self, text: str) -> List[str]:
        if self.split_mode == "character":
            return self._split_by_character(text)
        elif self.split_mode == "paragraph":
            return self._split_by_paragraph(text)
        else:
            raise ValueError(f"Unknown split_mode: {self.split_mode}")

    def _split_by_character(self, text: str) -> List[str]:
        chunks = []
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
            chunks.append(text[i : i + self.chunk_size])
        return chunks

    def _split_by_paragraph(self, text: str) -> List[str]:
        # Split on " \n" (space followed by newline) as a paragraph delimiter
        # This works better than "\n" alone but still can't reliably find paragraphs
        paragraphs = text.split(" \n")

        # Clean up: replace remaining single newlines within paragraphs with literal \n
        paragraphs = [para.replace("\n", "\\n").strip() for para in paragraphs]

        chunks = []
        current_chunk = ""

        for para in paragraphs:
            if not para:
                continue
            # If adding this paragraph exceeds chunk_size, save current and start new
            if len(current_chunk) + len(para) + 2 > self.chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                # Keep overlap by starting with end of previous chunk
                current_chunk = current_chunk[-self.chunk_overlap:] if self.chunk_overlap else ""

            current_chunk += para + "\n\n"

        # Don't forget the last chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks

    def split_texts(self, texts: List[str]) -> List[str]:
        chunks = []
        for text in texts:
            chunks.extend(self.split(text))
        return chunks

    def split_texts_with_metadata(self, texts_with_metadata: List[Tuple[str, str]]) -> Tuple[List[str], List[dict]]:
        """Split texts while preserving source metadata.

        Args:
            texts_with_metadata: List of (text, source_name) tuples

        Returns:
            Tuple of (chunks, metadata_list) where each chunk has corresponding metadata
        """
        chunks = []
        metadata_list = []
        for text, source in texts_with_metadata:
            text_chunks = self.split(text)
            chunks.extend(text_chunks)
            metadata_list.extend([{"source": source} for _ in text_chunks])
        return chunks, metadata_list


if __name__ == "__main__":
    loader = TextFileLoader("data/KingLear.txt")
    loader.load()
    splitter = CharacterTextSplitter()
    chunks = splitter.split_texts(loader.documents)
    print(len(chunks))
    print(chunks[0])
    print("--------")
    print(chunks[1])
    print("--------")
    print(chunks[-2])
    print("--------")
    print(chunks[-1])
