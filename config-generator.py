import argparse
import yaml
from yaml import CLoader as Loader, CDumper as Dumper
from jinja2 import Environment, FileSystemLoader

def main(template_file, source_file):
    #Load data from YAML file into Python dictionary
    device_variables = yaml.load(open(source_file), Loader=Loader)

    #Load Jinja2 template
    env = Environment(loader = FileSystemLoader('./'), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(template_file)

    #Render template using data and print the output
    config = template.render(device_variables)
    hostname = device_variables['hostname']
    if (write_config_to_file(config, hostname)):
        print(f"Configuration generated successfully. File is at ./{hostname}.txt")
    else:
        print("Error generating configuration.")

def write_config_to_file(config, filename):
    # config should be a string format
    try:
        f = open(f"{filename}.txt", "w")
        f.write(config)
        return True
    except:
        return False
    finally:
        f.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate device configurations from templates.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("-s", "--source", type=str, help="Path to file containing source data (.yaml).")
    parser.add_argument(
        "-t",
        "--template",
        type=str,
        help="Path to file containing Jinja template (.j2).",
    )
    args = parser.parse_args()

    main(
        template_file=args.template,
        source_file=args.source
    )
