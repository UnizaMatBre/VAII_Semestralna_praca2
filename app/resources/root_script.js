const ContentElement 		= document.getElementById("content");
const ProjectList 			= document.getElementById("project-list");
		
		
function unselect() {
	fetch("projects", {"method": "GET"})
	.then((response) => { 
		return response.json(); 
	})
	.then((data) => {
		options = "";
					
		data.forEach( (item) => {
					
			options +=  "<option value=" + item["rowid"] + ">" + item["name"] + "</option>";
						
		});
						
		options += "<option value='' selected disabled hidden>Select...</option>" 
		ContentElement.innerHTML = "<h2>No project selected</h2>";
			
		ProjectList.innerHTML = options;  
			
	});
}
		
function selectProject(rowid){
			
	fetch("projects", {"method": "GET"})
		.then((response) => { return response.json() })
		.then((data) => {
						
			selected = null;
						
			options = "";
						
			data.forEach( (item) => {
				if(item["rowid"] == rowid ) {
					selected = item
								
					return;
				}
								
						
				options += "<option value=" + item["rowid"] + ">" + item["name"] + "</option>";
						
			});
						
			// no selected project? Show prompt to select project
			if(selected == null) {
				
				options += "<option value='' selected disabled hidden>Select...</option>"
							
				ContentElement.innerHTML = "<h2>No project selected</h2>";
			}
			else {
				options = "<option value=''>..unselect..</option>" + options;
					
				options += "<option value=" + selected["rowid"] + " selected disabled hidden>" + selected["name"] + "</option>";

				fillContent(selected);
			};
					
			ProjectList.innerHTML = options;  
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
	
	ProjectList.addEventListener("change", (eventObj) => {
		
		
		let val = ProjectList.value;
		
		if (val === ""){
			unselect();
		}
		else {
			selectProject(val);
		}
		
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

function delProject(rowid) {
	
	fetch("projects?" +  new URLSearchParams({
		"rowid": rowid
	}), 
	{
		"method": "DELETE"
	})
	.then( (data) => { 
		unselect();
	});
	
	
}

function fillContent(project) {
	let headElem = "<div class='content-head'>";
	
	headElem += "<h2>" + project["name"] + "</h2>";
	
	headElem += project["description"];
	
	headElem += "<button class='task-delete-btn' onclick='delProject(" + project["rowid"] + ")'>X</button>";
	
	headElem += "</div>";
	
	
	let bodyElem = "<div class='content-body'>";
	
	project["tasks"].forEach( (taskObj) => {
		bodyElem += "<div class='task-class'>"; 
		
			bodyElem += "<div class='task-header'>";
		
				bodyElem += "<h2>"
		
				bodyElem += taskObj["rowid"];
		
				bodyElem += "</h2>";

				bodyElem += "<button class='task-delete-btn' onclick='delTask(" + taskObj["rowid"] + ")'>X</button>";
		
			bodyElem += "</div>";
		
		
			bodyElem += "<div class='task-body'>";
		
				bodyElem += taskObj["content"];
		
				bodyElem += "<select id='status' name='status' class='task-selector'>";	
		
				["open", "closed"].forEach( (statusVal) => {
					bodyElem += "<option value ='" + statusVal + "'>" + statusVal + "</option>";

				});
		
				bodyElem += "</select>"
		
			bodyElem += "</div>";

		bodyElem += "</div>"; 
		
		

	});
	
	bodyElem += "</div>";
	
	ContentElement.innerHTML = headElem + bodyElem;
	
	
}