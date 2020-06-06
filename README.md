# Thing

[WIP]

Tiny command line application for simple work with Things 3 app tasks and projects.

## Requirements

- Python 3.8+

```shell script
~ python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

> Note: you should have installed [Things 3](https://culturedcode.com/things/) app on your Mac, of course :)

## Basic usage

### Show Areas
```
~ python thing list areas

58B8D313-F899-4EB0-B143-3BC9F1D5210E  Education
307870E6-A8E2-4FBF-B365-A928D4BF3C89  Freelance
```

### List Projects
```
~ python thing list projects {area_uuid}
```
Example
```
~ python thing list projects 307870E6-A8E2-4FBF-B365-A928D4BF3C89

465263E9-2516-44AB-857A-1B57CF9EA55F  Test Project
```

### Show Project
```
~ python thing show project {project_uuid}
```
Example
```
~ python thing show project 465263E9-2516-44AB-857A-1B57CF9EA55F

Test Project
Project notes.

[x] Task 1
[ ] Task 2
```

### Export Project
```
~ python thing export project [project_uuid] {file,clipboard}
```
Example of export a project to clipboard
```
~ python thing export project 465263E9-2516-44AB-857A-1B57CF9EA55F clipboard
```
... then, paste it wherever you want.

Example of export a project to a file
```
~ python thing export project 465263E9-2516-44AB-857A-1B57CF9EA55F file project.md
```

## License
MIT