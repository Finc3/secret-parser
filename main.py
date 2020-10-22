import os, re, argparse


def parser(filename, secret_name, secret_value, format_prefix_postfix):
    """
    Parse the UTF-8 file and replace secret references with values from secrets dictionary.
    """
    print("Attempting to parse file: " + filename)
    with open('/github/workspace/' + filename, 'r') as fd:
        contents = fd.read()
    references = re.findall(f"(\${format_prefix_postfix} secrets.\w+ {format_prefix_postfix})", contents)
    reference_names = [re.findall(f"\${format_prefix_postfix} secrets.(\w+) {format_prefix_postfix}", x)[0] for x in references]
    index = reference_names.index(secret_name)
    contents = secret_value.join(contents.split(references[index]))
    with open('/github/workspace/' + filename, 'w') as fd:
        fd.write(contents)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser("Parse GitHub Actions secrets")
    argparser.add_argument('filename', help='file to parse')
    argparser.add_argument('secret_name', help='name of secret to search for')
    argparser.add_argument('secret_value', help='value of secret to replace name with')
    argparser.add_argument('format_prefix_postfix', help="the format for the replacement string")
    args = argparser.parse_args()
    parser(args.filename, args.secret_name, args.secret_value, args.format_prefix_postfix)