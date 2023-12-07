

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
	"""