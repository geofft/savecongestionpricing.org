#!venv/bin/python3

import pathlib
import shutil

import jinja2
import markdown_it


def get_env():
    md = markdown_it.MarkdownIt()
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader("site"),
        autoescape=jinja2.select_autoescape(),
        keep_trailing_newline=True,
    )
    env.filters["markdown"] = md.render
    return env


def main():
    env = get_env()

    site = pathlib.Path("site")
    output = pathlib.Path("output")
    shutil.rmtree(output, ignore_errors=True)

    for sitepath in list(site.glob("**/*")):
        path = pathlib.Path(*sitepath.parts[1:])
        if path.name[0] in "_.":
            continue
        contents = env.get_template(str(path)).render()
        outpath = output / path
        outpath.parent.mkdir(parents=True, exist_ok=True)
        outpath.write_text(contents)


if __name__ == "__main__":
    main()
