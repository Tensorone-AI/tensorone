<div class="fixed inset-0 z-[-1] overflow-hidden">
	<!-- Main dark background -->
	<div class="absolute inset-0 bg-black"></div>

	<!-- Green light source in bottom right corner -->
	<div
		class="absolute bottom-0 right-0 w-[800px] h-[800px] translate-x-[400px] translate-y-[400px]"
	>
		<!-- Core bright green light -->
		<div class="absolute inset-0 bg-kedua rounded-full blur-[100px]"></div>
		<!-- Secondary glow layer -->
		<div class="absolute inset-0 bg-kedua rounded-full blur-[150px] scale-125"></div>
		<!-- Outer diffuse glow -->
		<div class="absolute inset-0 bg-kedua rounded-full blur-[200px] scale-150"></div>
	</div>
	<!-- Final backdrop blur for depth -->
	<div class="absolute inset-0 backdrop-blur-[2px]"></div>
</div>
