const ContentElement 		= document.getElementById("content");
const SelectedProjectBttn 	= document.getElementById("selected-project-button");
const ProjectList 			= document.getElementById("project-list");
		
		
function unselect() {
	fetch("projects", {"method": "GET"})
	.then((response) => { 
		return response.json(); 
	})
	.then((data) => {
		buttons = "";
					
		data.forEach( (item) => {
					
			buttons +=  "<button onclick=\"selectProject(" + item["rowid"] + ")\">" + item["name"] + "</button>";
						
		});
						
		SelectedProjectBttn.innerHTML = "Select...";
		ContentElement.innerHTML = "<h2>No project selected</h2>";
			
		ProjectList.innerHTML = buttons;  
			
	});
}
		
function selectProject(rowid){
			
	fetch("projects", {"method": "GET"})
		.then((response) => { return response.json() })
		.then((data) => {
						
			selected = null;
						
			buttons = "";
						
			data.forEach( (item) => {
				if(item["rowid"] == rowid ) {
					selected = item
								
					return;
				}
								
						
				buttons +=  "<button onclick=\"javascript:selectProject(" + item["rowid"] + ")\">" + item["name"] + "</button>";
						
			});
						
						// no selected project? Show prompt to select project
			if(selected == null) {
							
				SelectedProjectBttn.innerHTML = "Select...";
				ContentElement.innerHTML = "<h2>No project selected</h2>";
			}
			else {
				buttons = "<button onclick=javascript:unselect()>= unselect =</button>" + buttons;
							
				SelectedProjectBttn.innerHTML = selected["name"];
							
				ContentElement.innerHTML = selected["tasks"];
				
				fillContent(selected);
			};
					
			ProjectList.innerHTML = buttons;  
		});
};
		
window.addEventListener("load", (event) => {
	unselect();
			
				// new project button event
	document.getElementById("new-project-button").addEventListener("click", (event) => {
	fetch("?action=projectmaker", {
		"method": "GET"
	})
	.then( (response) => {
		return response.text();
	})
	.then( (data) => { 
		document.getElementById("content").innerHTML = data;
						
		document.getElementById("project-make-form").addEventListener("submit", (eventObj) => {
			eventObj.preventDefault();
							
			let name = document.getElementById("project-name").value;
			let desc = document.getElementById("project-desc").value;
			
			
			fetch("projects", {
				"method": "POST",
				"body": JSON.stringify({
					"name": name,
					"description": desc
				})
			})
			.then( (response) => {
				return response.json();
			})
			.then( (data) => { 
				selectProject(parseInt(data["rowid"]));
			});
		});
	});
	});
});
			
const submit = function(event) {
				
	let name = document.getElementById("project-name").value;
	let desc = document.getElementById("project-desc").value;
			
			
	fetch("projects", {
		"method": "POST",
		"body": JSON.stringify({
			"name": name,
			"description": desc
		})
	})
	.then( (data) => { 
		console.log(data);
				
		selectProject(data["rowid"])
	});
};


function fillContent(project) {
	let headElem = "<div id='content-head'>";
	
	headElem += "<h2>" + project["name"] + "</h2>";
	
	headElem += project["description"];
	
	headElem += "</div>";
	
	
	let bodyElem = "<div id='content-body'>";
	
	project["tasks"].forEach( (taskObj) => {
		bodyElem += "<div>";
		
		bodyElem += "<div>";
		
		bodyElem += "<h5>"
		
		bodyElem += taskObj["rowid"];
		
		bodyElem += "</h5>";

		bodyElem += "<select id='status' name='status'>";	
		
		["open", "closed"].forEach( (statusVal) => {
			bodyElem += "<option value ='" + statusVal + "'>" + statusVal + "</option>";

		});
		
		bodyElem += "</select>"


		bodyElem += "<button id='task-delete-btn' onclick='delTask(" + taskObj["rowid"] + ")'></button>";
		
		bodyElem += "</div>";
		
		
		bodyElem += "<div>";
		
		bodyElem += taskObj["content"];
		
		bodyElem += "</div>";

		bodyElem += "</div>"; 
		
		

	});
	
	bodyElem += "</div>";
	
	ContentElement.innerHTML += headElem + bodyElem;
	
	
}