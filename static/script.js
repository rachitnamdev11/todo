const API = "/tasks"

async function loadTasks(){

let res = await fetch(API)
let tasks = await res.json()

let list = document.getElementById("taskList")

list.innerHTML=""

tasks.forEach(task=>{

let li = document.createElement("li")

if(task.completed){
li.classList.add("completed")
}

li.innerHTML = `
<span onclick="toggleTask('${task.id}')">
${task.title}
</span>

<button onclick="deleteTask('${task.id}')">Delete</button>
`

list.appendChild(li)

})

}

async function addTask(){

let input = document.getElementById("taskInput")

let title = input.value

if(title=="") return

await fetch(API,{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({title})
})

input.value=""

loadTasks()

}


async function toggleTask(id){

await fetch(`/tasks/${id}`,{
method:"PUT"
})

loadTasks()

}


async function deleteTask(id){

await fetch(`/tasks/${id}`,{
method:"DELETE"
})

loadTasks()

}


loadTasks()