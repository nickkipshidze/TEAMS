import os, sys

BASE_DIR = os.path.dirname(sys.argv[0]) if os.path.dirname(sys.argv[0]) != "" else "."

class Tasks:
    def __init__(self, tasksfile):
        self.tokens = {
            "[ ]": "Empty",
            "[+]": "Completed",
            "[-]": "Missed",
            "[!]": "Cancelled",
            "[x]": "Overwork"
        }
        self.html_checkboxes = {
            "[ ]": "<span class=\"chk empty\"></span>",
            "[+]": "<span class=\"chk finished\"></span>",
            "[-]": "<span class=\"chk missed\"></span>",
            "[!]": "<span class=\"chk cancelled\"></span>",
            "[x]": "<span class=\"chk overwork\"></span>"
        }
        
        self.tasksfile = tasksfile
        self.rawtasks = open(tasksfile, "r").read()
        self.tasks = self.parse(
            self.rawtasks
        )
        
    def parse(self, rawtasks):
        rawdays = rawtasks.split("---")
        if "" in rawdays: rawdays.remove("")
        
        tasks = {}
            
        for rawday in rawdays:
            lines = rawday.split("\n")
            for _ in range(lines.count("")): lines.remove("")
            
            date = lines[0][2:]
            tasks[date] = []
            
            for line in lines[1:]:
                if line[0:2] == "- ":
                    tasks[date].append({
                        "heading": line[2:],
                        "tasks": []
                    })
                elif line[0:3] in self.tokens:
                    tasks[date][-1]["tasks"].append(line)
        
        return tasks

    def getcode(self, targetdate):
        rawdays = self.rawtasks.split("---")
        if "" in rawdays: rawdays.remove("")
        
        for rawday in rawdays:
            lines = rawday.split("\n")
            for _ in range(lines.count("")): lines.remove("")
            
            date = lines[0][2:]
            if date == targetdate:
                return rawday
        
        return ""
    
    def add(self, newsource):
        open(self.tasksfile, "w").write(
            newsource + self.rawtasks
        )
        self.rawtasks = open(self.tasksfile, "r").read()
    
    def update(self, targetdate, newsource):
        rawdays = self.rawtasks.split("---")
        if "" in rawdays: rawdays.remove("")
        
        for rawday in rawdays:
            lines = rawday.split("\n")
            for _ in range(lines.count("")): lines.remove("")
            
            date = lines[0][2:]
            if date == targetdate:
                rawdays[rawdays.index(rawday)] = newsource
        
        open(self.tasksfile, "w").write(
            "---".join(rawdays)
        )
        
    def html(self, tasks=None):
        if tasks == None:
            tasks = self.tasks
            
        html = ""
            
        for date, sections in tasks.items():
            day_template = "<div class=\"day-container\"><div><h1>{date}</h1>{sections}</div>{menu}</div>"
            section_template = "<div class=\"day-section\"><h2>{section}</h2>{tasks}</div>"
            task_template = "<p>{task}</p>"
            
            html_sections = ""
            for section in sections:
                html_tasks = ""
                for task in section["tasks"]:
                    for checkbox, element in self.html_checkboxes.items():
                        task = task.replace(checkbox, element)
                    html_tasks += task_template.format(task=task)
                html_sections += section_template.format(section=section["heading"], tasks=html_tasks)
            html += day_template.format(date=date, sections=html_sections, menu=open(f"{BASE_DIR}/static/section-menu.html", "r").read())

        return html

    def html_day(self, day):
        html = ""
        
        for date, sections in day.items():
            day_template = "<h1>{date}</h1>{sections}"
            section_template = "<div class=\"day-section\"><h2>{section}</h2>{tasks}</div>"
            task_template = "<p>{task}</p>"
            
            html_sections = ""
            for section in sections:
                html_tasks = ""
                for task in section["tasks"]:
                    for checkbox, element in self.html_checkboxes.items():
                        task = task.replace(checkbox, element)
                    html_tasks += task_template.format(task=task)
                html_sections += section_template.format(section=section["heading"], tasks=html_tasks)
            html += day_template.format(date=date, sections=html_sections)
        
        return html