# High-Compression Zstandard Archiver

A powerful command-line utility written in Python for creating and extracting highly compressed archives of directories using the **Zstandard (Zstd)** compression algorithm combined with the **tar** archiving format.

This tool is designed for users who require **maximum compression** and **fast processing** of large datasets or project folders, leveraging Zstd's superior performance characteristics and multi-threading capabilities.

## 🌟 Features

*   **High-Performance Compression:** Utilizes the Zstandard algorithm, known for its excellent balance of compression ratio and speed.
*   **Directory Archiving:** Seamlessly archives entire directories into a single `.tar.zst` file.
*   **Adjustable Compression Level:** Supports compression levels from 1 (fastest) to 22 (maximum compression).
*   **Multi-Threading Support:** Leverages all available CPU cores by default for significantly faster compression times.
*   **Simple Command-Line Interface:** Easy-to-use interface with dedicated `compress` and `extract` commands.

## 🛠️ Prerequisites

To run this script, you need:

*   **Python 3.6+**
*   The `zstandard` library, which provides the Python bindings for Zstd.

## 📦 Installation

1.  **Download the script:**
    ```bash
    wget "https://raw.githubusercontent.com/mohammedelgamal/High-Compression-Zstandard-Archiver/main/main.py" -OutFile "main.py"
    mv main.py zstd_archiver.py
    ```

2.  **Install the required library:**
    The core dependency is the `zstandard` library.

    ```bash
    pip install zstandard
    ```

## 🚀 Usage

The script uses a sub-command structure for its two main operations: `compress` and `extract`.

### General Syntax

```bash
python zstd_archiver.py <command> [arguments]
```

### 1. Compressing a Directory

Use the `compress` command to archive a folder into a `.tar.zst` file.

#### Syntax

```bash
python zstd_archiver.py compress <input_dir> <output_file> [options]
```

| Argument | Description | Required | Default |
| :--- | :--- | :--- | :--- |
| `<input_dir>` | The path to the folder you want to compress. | Yes | N/A |
| `<output_file>` | The desired name for the output `.tar.zst` archive. | Yes | N/A |
| `-l`, `--level N` | Compression level (1=fastest, 22=max compression). | No | 22 |
| `-t`, `--threads N` | Number of threads to use (-1 for all available cores, 0 for single-threaded). | No | -1 |

#### Example: Maximum Compression (Default)

This command compresses the `/path/to/my_project` folder into `my_project_archive.tar.zst`, using the default maximum compression level (22) and all available threads.

```bash
python zstd_archiver.py compress /path/to/my_project my_project_archive.tar.zst
```

#### Example: Faster Compression with Specific Level

This command compresses the folder using compression level 10 and restricts the process to 4 threads.

```bash
python zstd_archiver.py compress /path/to/data_dump data_dump.tar.zst --level 10 --threads 4
```

### 2. Extracting an Archive

Use the `extract` command to decompress and extract a `.tar.zst` archive into a specified directory.

#### Syntax

```bash
python zstd_archiver.py extract <input_file> <output_dir>
```

| Argument | Description | Required | Default |
| :--- | :--- | :--- | :--- |
| `<input_file>` | The path to the `.tar.zst` archive to extract. | Yes | N/A |
| `<output_dir>` | The destination directory where the contents will be extracted. | Yes | N/A |

#### Example

This command extracts the contents of `my_project_archive.tar.zst` into the `/tmp/extracted_data` directory. The directory will be created if it does not exist.

```bash
python zstd_archiver.py extract my_project_archive.tar.zst /tmp/extracted_data
```

## ⚙️ Technical Implementation

The script employs a **streaming approach** to combine the `tarfile` and `zstandard` libraries efficiently.

1.  **Compression:** The script opens the output file in binary write mode (`'wb'`). It then wraps this file object with a `zstd.ZstdCompressor().stream_writer()`. Finally, it passes this compressed stream to `tarfile.open(..., mode='w|')`. This ensures that the tar archive is written directly into the Zstd compression stream, minimizing memory usage and maximizing throughput.
2.  **Extraction:** A similar streaming technique is used in reverse. The input file is read, wrapped in a `zstd.ZstdDecompressor().stream_reader()`, and then passed to `tarfile.open(..., mode='r|')` for extraction.

This method is highly efficient for handling very large files and directories.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details (if applicable).

---
*Authored by Mohamed M. Elgamal*
