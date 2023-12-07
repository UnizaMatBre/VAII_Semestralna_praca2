

def View(data):
    return r"""
    <!DOCTYPE html>
    <html lang="en">
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0"> 
			
		<link rel="stylesheet" href="main_styles.css">
		
		<title>First Page</title>
	</head>
	
	<body>
		<div class="side-main-menu">
			<a>Help</a>
			<a>Credits</a>
		</div>
	
		<div class="project-selector"> 
			<div>
				<select id="project-list" class="selectable-projects"></select>
				<button id="new-project-button">New project...</Button>
			</div>
		</div>
		
		
		
		<div id="content" class="main-content">

		</div>
		
		
		
		<script src="root_script.js"></script>
	</body>
   </html>
	"""
    
