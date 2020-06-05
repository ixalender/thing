# Thing

[WIP]

Tiny commandline application for simple work with Things3 app taks and projects.

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

### Export Project
```
~ python thing export project [project_uuid] {file,clipboard}
```
Example of export to clipboard
```
~ python thing export project 465263E9-2516-44AB-857A-1B57CF9EA55F clipboard
```
.. then, paste it wherever you want.

Example of export to a file
```
~ python thing export project 465263E9-2516-44AB-857A-1B57CF9EA55F file project.md
```
