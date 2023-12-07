

def View(data):
	return r"""
	<form id="project-make-form">
	<ul>
		<li><label for="project-name">Name of the project?</label>
		<input type="text" id="project-name" required /></li>
		
		<li><label for="project-desc">Description</label>
		<input type="text" id="project-desc" value="" /></li>
	
		<li><input type="submit" value="Create" /></li>
	</ul>
	</form>
	
	
	<script>
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
	</script>
	"""