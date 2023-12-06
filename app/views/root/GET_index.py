

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
			<div id="project-list" class="selectable-projects"></div>
		</div>
		
		
		
		<div id="content" class="main-content">
			<h1>Lorem Ipsum</h1>
		
			
			Praesent dolor nibh, interdum quis consectetur vitae, egestas et ante. Nulla interdum urna justo. Aliquam nisl ex, consequat eget porttitor quis, imperdiet non ante. Nulla et mauris eget neque pretium consequat. Morbi vulputate in est malesuada fringilla. Curabitur ac auctor magna. Nulla facilisi. Sed lobortis felis sed ultrices malesuada. Suspendisse tincidunt turpis turpis, nec malesuada ex dictum et. Fusce cursus nunc et sem rhoncus varius. Maecenas nec metus velit. Nulla tincidunt pellentesque maximus. Phasellus et luctus massa.
			Quisque dignissim egestas eros sed auctor. Quisque suscipit augue vitae libero mattis, vel blandit tellus consectetur. Quisque sit amet ligula efficitur, convallis purus id, bibendum neque. Nunc rhoncus fringilla neque ac convallis. Donec et ex molestie, accumsan urna nec, malesuada lacus. Quisque gravida nulla lectus, vel viverra lacus tempor non. Vestibulum consequat ante sit amet nulla lacinia ullamcorper. Sed vehicula faucibus venenatis. Maecenas nec purus a metus sodales euismod in in est.
			Donec ut libero a ex finibus accumsan ac at quam. Curabitur at est pulvinar, tempus lorem ut, facilisis urna. Nam sed porta massa. Aliquam arcu eros, porttitor vitae diam vel, auctor posuere libero. Mauris tempus pharetra diam at consequat. Aenean luctus tincidunt ligula sit amet maximus. Fusce sed odio consequat, blandit lacus vel, condimentum nisi. Fusce placerat, ex quis maximus euismod, augue quam suscipit sem, et aliquam odio odio non massa. Nulla facilisi. Vestibulum eu odio facilisis, laoreet lorem id, lacinia nunc. Maecenas in augue volutpat, mattis velit sed, gravida massa. 
		</div>
		
	</body>
    </html>
    """
    