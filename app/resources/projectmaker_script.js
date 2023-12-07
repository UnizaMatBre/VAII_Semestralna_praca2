document.getElementById("project-make-form").addEventListener("submit", function(event) {
	event.preventDefault();
			
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
});