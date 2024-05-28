"use strict"

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