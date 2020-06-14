# Thing

Tiny command line application for simple work with Things 3 app tasks and projects.

## Requirements

- Python 3.8+

```shell script
~ python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

> Note: you should have [Things 3](https://culturedcode.com/things/) installed on your Mac.

## Basic usage

### List Areas
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

### List Tasks
```
~ python thing list tasks {project_uuid}
```
Example
```
~ python thing list tasks 465263E9-2516-44AB-857A-1B57CF9EA55F

E360FBD9-483A-47F8-B39E-AA1DB342DAF9 [x] do something
3E7EDAF4-2BFD-4DFC-9EDF-EA1CFD96ED01 [x] do something else
BD7D3CA3-4F7D-494E-BF32-6DC8AFE93D57 [ ] do not do anything

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

[x] do something
[x] do something else
[ ] do not do anything
```

### Show Task
```
~ python thing show project {project_uuid}
```
Example
```
~ python thing show task BD7D3CA3-4F7D-494E-BF32-6DC8AFE93D57

[ ] do not do anything
---
Because I don't want to be tired.

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