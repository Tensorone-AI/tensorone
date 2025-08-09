<script>
	import { scale, fade } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
	import AudioVisualizer from './AudioVisualizer.svelte';

	export let voiceLevel = 0;
	export let statusText = '';
	export let isListening = false;
	export let isProcessing = false;
	export let isAgentSpeaking = false;
	export let microphoneStream = null;
	export let startListening = () => {};
	export let stopListening = () => {};
	export let startCallModeRecording = () => {};
	export let stopCallModeRecording = () => {};
	export let stopCurrentAudio = () => {};
	export let hasCallFeature = false;
	export let handleBackToChat = () => {};
</script>

<div class="flex flex-col items-center justify-center h-full relative">
	<!-- Three.js Audio Visualizer - Center of screen -->
	<div class="absolute inset-0">
		<AudioVisualizer
			{microphoneStream}
			{isListening}
			{isProcessing}
			{isAgentSpeaking}
		/>
	</div>

	<!-- Control Buttons -->
	<div
		in:fade|global={{ delay: 300, duration: 500 }}
		out:fade|global={{ duration: 300 }}
		class="absolute bottom-8 left-1/2 transform -translate-x-1/2 flex gap-6"
	>
		<!-- Microphone Button -->
		<button
			class="3xl:w-16 3xl:h-16 w-12 h-12 rounded-full flex items-center justify-center transition-all duration-200 hover:opacity-70 disabled:opacity-50 {isListening
				? 'bg-[#F80036]'
				: 'bg-utama'}"
			on:click={() => {
				if (isListening) {
					if (hasCallFeature) {
						stopCallModeRecording();
					} else {
						stopListening();
					}
				} else {
					if (isAgentSpeaking) {
						stopCurrentAudio();
					} else if (hasCallFeature) {
						startCallModeRecording();
					} else {
						startListening();
					}
				}
			}}
			disabled={isProcessing}
			title={isListening ? 'Stop listening' : isAgentSpeaking ? 'Stop AI speech' : 'Start listening'}
		>
			{#if isListening}
				<!-- Stop icon when listening -->
				<svg
					width="24"
					height="24"
					viewBox="0 0 24 24"
					fill="none"
					xmlns="http://www.w3.org/2000/svg"
				>
					<rect x="6" y="6" width="12" height="12" rx="2" fill="black" />
				</svg>
			{:else}
				<!-- Microphone icon when not listening -->
				<svg
					width="24"
					height="24"
					viewBox="0 0 24 24"
					fill="none"
					xmlns="http://www.w3.org/2000/svg"
				>
					<path
						d="M12 1C10.9 1 10 1.9 10 3V12C10 13.1 10.9 14 12 14C13.1 14 14 13.1 14 12V3C14 1.9 13.1 1 12 1Z"
						fill="black"
					/>
					<path
						d="M19 10V12C19 15.9 15.9 19 12 19C8.1 19 5 15.9 5 12V10H7V12C7 14.8 9.2 17 12 17C14.8 17 17 14.8 17 12V10H19Z"
						fill="black"
					/>
					<path d="M10 21H14V23H10V21Z" fill="black" />
				</svg>
			{/if}
		</button>

		<!-- Back to Chat Button -->
		<button
			class="3xl:w-16 3xl:h-16 w-12 h-12 rounded-full flex items-center justify-center bg-[#1F222D] hover:opacity-70 transition-all duration-200"
			on:click={handleBackToChat}
			disabled={isListening || isProcessing || isAgentSpeaking}
			title="Go back to chat"
		>
			<svg
				width="24"
				height="24"
				viewBox="0 0 24 24"
				fill="none"
				xmlns="http://www.w3.org/2000/svg"
			>
				<path
					d="M20 2H4C2.9 2 2 2.9 2 4V16C2 17.1 2.9 18 4 18H8L12 22L16 18H20C21.1 18 22 17.1 22 16V4C22 2.9 21.1 2 20 2Z"
					stroke="#ECF2FF"
					stroke-width="2"
					fill="none"
					stroke-linecap="round"
					stroke-linejoin="round"
				/>
				<path d="M8 9H16" stroke="#ECF2FF" stroke-width="2" stroke-linecap="round" />
				<path d="M8 13H14" stroke="#ECF2FF" stroke-width="2" stroke-linecap="round" />
			</svg>
		</button>
	</div>
</div>
