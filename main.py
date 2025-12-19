import argparse
import tarfile
import zstandard as zstd
import os

def compress_folder_zstd(folder_path, output_filepath, level, threads):
    """Compresses a folder and its contents using Zstandard."""
    print(f"Starting Zstd compression of '{folder_path}' using {threads if threads != -1 else 'all available'} threads...")
    print(f"Output file: {output_filepath}, Level: {level}")
    
    # Initialize the Zstd compressor with the user-defined level and threads
    cctx = zstd.ZstdCompressor(level=level, threads=threads)
    
    try:
        with open(output_filepath, 'wb') as f_out:
            # Create a compressed I/O stream
            with cctx.stream_writer(f_out) as compress_stream:
                with tarfile.open(fileobj=compress_stream, mode='w|') as tar:
                    # Add the folder recursively.
                    tar.add(folder_path, arcname=os.path.basename(folder_path))
        print("Compression complete! :)")
    except FileNotFoundError:
        print(f"Error: Input folder '{folder_path}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Function for Decompression (Extraction)

def decompress_folder_zstd(input_filepath, output_dir):
    """Decompresses a Zstandard archive into a directory."""
    print(f"Starting Zstd extraction of '{input_filepath}' to '{output_dir}'...")
    dctx = zstd.ZstdDecompressor()
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        with open(input_filepath, 'rb') as f_in:
            # Create a decompressed I/O stream
            with dctx.stream_reader(f_in) as decompress_stream:
                with tarfile.open(fileobj=decompress_stream, mode='r|') as tar:
                    # Extract all contents
                    tar.extractall(path=output_dir)
        print("Extraction complete! :)")
    except FileNotFoundError:
        print(f"Error: Input file '{input_filepath}' not found.")
    except zstd.ZstdError:
        print(f"Error: Failed to decompress. File may be corrupted or not a valid Zstandard archive.")
    except Exception as e:
        print(f"An unexpected error occurred during extraction: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="A high-compression Zstandard archiver (Compress/Extract)."
    )
    # Use subparsers for COMPRESS and EXTRACT modes
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- COMPRESS Subparser ---
    compress_parser = subparsers.add_parser("compress", help="Compress a directory into a .tar.zst file.")
    compress_parser.add_argument(
        "input_dir", type=str, help="The folder/directory to be compressed."
    )
    compress_parser.add_argument(
        "output_file", type=str, help="The name of the output .tar.zst archive."
    )
    compress_parser.add_argument(
        "-l", "--level", type=int, default=22, choices=range(1, 23), metavar='N',
        help="Compression level (1=fastest, 22=max compression). Default is 22."
    )
    compress_parser.add_argument(
        "-t", "--threads", type=int, default=-1,
        help="Number of compression threads (0=single-threaded, -1=all available cores). Default is -1."
    )

    # --- EXTRACT Subparser ---
    extract_parser = subparsers.add_parser("extract", help="Extract a .tar.zst file into a directory.")
    extract_parser.add_argument(
        "input_file", type=str, help="The path to the .tar.zst archive to extract."
    )
    extract_parser.add_argument(
        "output_dir", type=str, help="The destination directory for extracted files."
    )

    args = parser.parse_args()

    if args.command == "compress":
        compress_folder_zstd(args.input_dir, args.output_file, args.level, args.threads)
    elif args.command == "extract":
        decompress_folder_zstd(args.input_file, args.output_dir)

if __name__ == "__main__":
    main()
