<script>
	import { fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
</script>

<div
	class="absolute -left-2"
	transition:fly={{ delay: 250, duration: 300, x: -20, opacity: 0.5, easing: quintOut }}
>
	<svg width="3" height="80" viewBox="0 0 3 80" fill="none" xmlns="http://www.w3.org/2000/svg">
		<rect width="3" height="80" fill="url(#paint0_linear_129_926)" style="" />
		<defs>
			<linearGradient
				id="paint0_linear_129_926"
				x1="0"
				y1="0"
				x2="3.32488e-08"
				y2="80"
				gradientUnits="userSpaceOnUse"
			>
				<stop style="stop-color:black;stop-opacity:1;" />
				<stop
					offset="0.495192"
					stop-color="#23F784"
					style="stop-color:#23F784;stop-color:color(display-p3 0.1373 0.9686 0.5176);stop-opacity:1;"
				/>
				<stop offset="1" style="stop-color:black;stop-opacity:1;" />
			</linearGradient>
		</defs>
	</svg>
</div>
