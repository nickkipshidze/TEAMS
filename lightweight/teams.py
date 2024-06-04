from http.server import HTTPServer, BaseHTTPRequestHandler
import json

STYLES = """
* {
    padding: 0;
    margin: 0;
}

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background-color: #2D333B;
}

::-webkit-scrollbar-thumb {
    background-color: #444C56;
    border-radius: 4px;
}

body {
    background-color: #242132;
    font-family: monospace;
}

a {
    color: blue;
    text-decoration: none;
}

textarea {
    display: relative;
    padding: 10px;
    width: 100%;
    height: auto;
    resize: none;
    background-color: #242132;
    outline: none;
    border: 1px solid #6D6B77;
    border-radius: 7px;
    color: #fff;
    box-sizing: border-box;
}

#add-btn {
    display: flex;
    height: 1px;
    align-items: center;
    justify-content: center;
    background-color: #363344;
    border: 1px solid #6D6B77;
    border-radius: 10px;
    padding: 20px;
    margin: 20px;
    cursor: pointer;
}

#add-btn > svg {
    width: 20px;
    height: 20px;
}

.day-container {
    display: flex;
    justify-content: space-between;
    background-color: #363344;
    border: 1px solid #6D6B77;
    border-radius: 10px;
    margin: 20px;
    padding: 20px;
}

.day-container > :first-child {
    width: 90%;
    box-sizing: border-box;
    color: #fff;
}

.day-container > :last-child {
    display: flex;
    width: 10%;
    justify-content: flex-end;
}

.day-container > .section-menu > svg {
    cursor: pointer;
    width: 20px;
    height: 20px;
}

.day-section {
    display: flex;
    margin-top: 10px;
    flex-direction: column;
    gap: 5px;
}

.day-section > h2 {
    color: #CE3DF3;
    padding-top: 5px;
}

.day-section > p {
    display: flex;
    align-items: center;
    gap: 5px;
}

.chk {
    display: flex;
    width: 12px;
    height: 12px;
    background-color: #fff;
    border-radius: 2px;
    border: 1px solid #6D6B77;
}

.chk.empty { background-color: transparent; }
.chk.finished { background-color: #05CC95; }
.chk.missed { background-color: #FF8737; }
.chk.cancelled { background-color: #837036; }
.chk.overwork { background-color: #00ff0d; }
"""

JAVASCRIPT = """"use strict"

document.querySelectorAll("#menubutton").forEach((element) => {
    element.addEventListener("click", async (event) => {
        let menuElement = undefined;
        if (event.target.parentElement.className != "section-menu")
            menuElement = event.target.parentElement.parentElement.parentElement
        else
            menuElement = event.target.parentElement
        
        let dayElement = menuElement.parentElement.firstChild
        
        if (dayElement.firstChild.id == "autoresizing") {
            let date = dayElement.firstChild.className
            let source = dayElement.firstChild.value
            
            let newhtml = await fetch("/save", {
                method: "POST",
                mode: "cors",
                cache: "no-cache",
                credentials: "same-origin",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    "date": date,
                    "source": source
                })
            })
            newhtml = await newhtml.json()
            newhtml = newhtml.html
            
            dayElement.innerHTML = newhtml      
        } else {
            let date = dayElement.firstChild.innerText
            
            let sourceCode = await fetch("/getcode", {
                method: "POST",
                mode: "cors",
                cache: "no-cache",
                credentials: "same-origin",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    "date": date
                })
            })
            sourceCode = await sourceCode.json()
            sourceCode = sourceCode.source
            
            dayElement.innerHTML = `<textarea id="autoresizing" class="${date}">${sourceCode}</textarea>`
            
            dayElement.firstChild.style.height = "auto"
            dayElement.firstChild.style.height = dayElement.firstChild.scrollHeight + "px"
        }
    })
})

document.getElementById("add-btn").addEventListener("click", async (event) => {
    await fetch("/add", {
        method: "POST",
        mode: "cors",
        cache: "no-cache",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "source": "> Untitled"
        })
    })
    window.location.reload()
})
"""

BASE_HTML = """<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
        <style>{style}</style>
    </head>
    <body>
        <div id="add-btn"><svg fill="#ffffff" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 45.402 45.402" xml:space="preserve" stroke="#ffffff"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <g> <path d="M41.267,18.557H26.832V4.134C26.832,1.851,24.99,0,22.707,0c-2.283,0-4.124,1.851-4.124,4.135v14.432H4.141 c-2.283,0-4.139,1.851-4.138,4.135c-0.001,1.141,0.46,2.187,1.207,2.934c0.748,0.749,1.78,1.222,2.92,1.222h14.453V41.27 c0,1.142,0.453,2.176,1.201,2.922c0.748,0.748,1.777,1.211,2.919,1.211c2.282,0,4.129-1.851,4.129-4.133V26.857h14.435 c2.283,0,4.134-1.867,4.133-4.15C45.399,20.425,43.548,18.557,41.267,18.557z"></path> </g> </g></svg></div>
        {body}
        <script>{script}</script>
    </body>
</html>
"""

SECTION_MENU_HTML = """<div class="section-menu">
    <svg id="menubutton" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" fill="#ffffff" class="bi bi-three-dots-vertical" stroke="#ffffff"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M9.5 13a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0zm0-5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0zm0-5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0z"></path> </g></svg>
</div>
"""

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
            html += day_template.format(date=date, sections=html_sections, menu=open("./static/section-menu.html", "r").read())

        return html

    def html_day(self, day):
        html = ""
        
        for date, sections in day.items():
            day_template = "<div><h1>{date}</h1>{sections}</div>"
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
            html += day_template.format(date=date, sections=html_sections, menu=open("./static/section-menu.html", "r").read())
        
        return html

class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            tasks = Tasks("tasks.tsk")
            response = open("./static/index.html", "r").read().format(body=tasks.html())
            
        elif self.path == "/static/style.css":
            self.send_response(200)
            self.send_header("Content-type", "text/css")
            response = open("./static/style.css", "r").read()
            
        elif self.path == "/static/script.js":
            self.send_response(200)
            self.send_header("Content-type", "text/javascript")
            response = open("./static/script.js", "r").read()
            
        else:
            self.send_response(404)
            response = "404 Not Found"
        
        self.end_headers()
        self.wfile.write(response.encode())
            
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode("utf-8"))
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid JSON")
            return None
        
        tasks = Tasks("tasks.tsk")
        
        if self.path == "/getcode":
            source = tasks.getcode(data["date"])
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            response = json.dumps({"source": source.strip("\n")})
            
        elif self.path == "/save":
            tasks.update(data["date"], "\n"+data["source"]+"\n")
            parsed = tasks.parse("---\n"+data["source"])
            html = tasks.html_day(parsed)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            response = json.dumps({"html": html})
                
        elif self.path == "/add":
            tasks.add("\n"+data["source"]+"\n---")
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            response = json.dumps({"html": tasks.html()})
                
        else:
            self.send_response(404)
            response = "404 Not Found"

        self.end_headers()
        self.wfile.write(response.encode())

serveraddr = ("", 8000)
httpd = HTTPServer(serveraddr, HTTPRequestHandler)
print("Starting server on port 8000...")
httpd.serve_forever()
