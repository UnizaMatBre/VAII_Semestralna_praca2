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
						document.getElementById("content").innerHTML = DOMParser().fr;
					});
				
				});
			
			
			});