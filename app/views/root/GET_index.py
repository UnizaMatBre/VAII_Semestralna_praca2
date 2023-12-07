

def View(data):
    return r"""
    <!DOCTYPE html>
    <html lang="en">
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0"> 
			
		<title>First Page</title>
	</head>
	
	<body>
		<div class="side-main-menu">
			<a>Help</a>
			<a>Credits</a>
		</div>
	
		<div class="project-selector"> 
			<button id="selected-project-button" class="main-button">Button Text</button>
			<div>
				<div id="project-list" class="selectable-projects"></div>
				<button id="new-project-button">New project...</Button>
			</div>
		</div>
		
		
		
		<div id="content" class="main-content">

		</div>
		
		
		
		<script src="root_script.js"></script>
	</body>
   </html>
	"""
    
