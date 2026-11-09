"""CLI interface for markwright."""
import argparse
import sys
from markwright.builder import SiteBuilder


def main():
    parser = argparse.ArgumentParser(description="Markwright - Static Site Generator")
    parser.add_argument("src_dir", help="Directory containing Markdown content")
    parser.add_argument("--output", "-o", default="dist", help="Target output HTML directory")

    args = parser.parse_args()
    builder = SiteBuilder(args.src_dir, args.output)
    count = builder.build()
    print(f"Successfully generated {count} pages into {args.output}")


if __name__ == "__main__":
    main()
