import argparse

def main():
    parser = argparse.ArgumentParser(
        prog="survey",
        description="Survey project utilities"
    )
    sub = parser.add_subparsers(dest="cmd", required=False)

    sub.add_parser("init", help="Initialize project from baseline survey")
    sub.add_parser("update", help="Update with Top-of-Pipe and/or Downhole")
    sub.add_parser("elevation", help="Generate point-elevation CSV")
    sub.add_parser("graphs", help="Generate graphs")

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        return 0
    print(f"Command selected: {args.cmd} (implementation pending)")
    return 0

if __name__ == "__main__":
    main()

