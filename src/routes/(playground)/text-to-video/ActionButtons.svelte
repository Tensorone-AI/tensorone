<script>
	export let toggleFullscreen;
	export let downloadVideo;
</script>

<div class="flex items-center justify-end gap-2">
	<button
		on:click={toggleFullscreen}
		class="px-4 py-2 bg-[#06070A] border border-[#444A61] rounded-full hover:opacity-70 transition-all duration-200 flex items-center gap-2"
	>
		<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
			<g clip-path="url(#clip0_376_2073)">
				<path
					d="M10.3999 0.800049H15.1999V5.60005"
					stroke="#ECF2FF"
					style="stroke:#ECF2FF;stroke:color(display-p3 0.9250 0.9475 1.0000);stroke-opacity:1;"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
				/>
				<path
					d="M5.60005 15.1999H0.800049V10.3999"
					stroke="#ECF2FF"
					style="stroke:#ECF2FF;stroke:color(display-p3 0.9250 0.9475 1.0000);stroke-opacity:1;"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
				/>
				<path
					d="M15.2001 0.800049L9.6001 6.40005"
					stroke="#ECF2FF"
					style="stroke:#ECF2FF;stroke:color(display-p3 0.9250 0.9475 1.0000);stroke-opacity:1;"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
				/>
				<path
					d="M0.800049 15.2001L6.40005 9.6001"
					stroke="#ECF2FF"
					style="stroke:#ECF2FF;stroke:color(display-p3 0.9250 0.9475 1.0000);stroke-opacity:1;"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
				/>
			</g>
			<defs>
				<clipPath id="clip0_376_2073">
					<rect width="16" height="16" fill="white" style="fill:white;fill-opacity:1;" />
				</clipPath>
			</defs>
		</svg>
		<span class="text-[#ECF2FF]">Fullscreen</span>
	</button>
	<button
		on:click={downloadVideo}
		class="px-4 py-2 bg-[#06070A] border border-[#444A61] rounded-full hover:opacity-70 transition-all duration-200 flex items-center gap-2"
	>
		<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
			<g clip-path="url(#clip0_376_2080)">
				<path
					d="M15.2 10.3999V13.5999C15.2 14.0242 15.0315 14.4312 14.7314 14.7313C14.4314 15.0313 14.0244 15.1999 13.6 15.1999H2.40005C1.9757 15.1999 1.56874 15.0313 1.26868 14.7313C0.96862 14.4312 0.800049 14.0242 0.800049 13.5999V10.3999"
					stroke="#ECF2FF"
					style="stroke:#ECF2FF;stroke:color(display-p3 0.9250 0.9475 1.0000);stroke-opacity:1;"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
				/>
				<path
					d="M4 6.3999L8 10.3999L12 6.3999"
					stroke="#ECF2FF"
					style="stroke:#ECF2FF;stroke:color(display-p3 0.9250 0.9475 1.0000);stroke-opacity:1;"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
				/>
				<path
					d="M8 10.4V0.800049"
					stroke="#ECF2FF"
					style="stroke:#ECF2FF;stroke:color(display-p3 0.9250 0.9475 1.0000);stroke-opacity:1;"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
				/>
			</g>
			<defs>
				<clipPath id="clip0_376_2080">
					<rect width="16" height="16" fill="white" style="fill:white;fill-opacity:1;" />
				</clipPath>
			</defs>
		</svg>
		<span class="text-[#ECF2FF]">Download</span>
	</button>
</div>
