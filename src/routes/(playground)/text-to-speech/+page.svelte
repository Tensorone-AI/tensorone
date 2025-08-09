<script>
	import { onMount, onDestroy } from 'svelte';
	import { fade } from 'svelte/transition';
	import Header from '../Header.svelte';
	import PageTitle from '../PageTitle.svelte';
	import VoiceResult from './VoiceResult.svelte';
	import TextInput from './TextInput.svelte';
	import VoiceClone from './VoiceClone.svelte';
	import PrebuiltVoices from './PrebuiltVoices.svelte';
	import GenerateButton from './GenerateButton.svelte';
	import HelpModal from './HelpModal.svelte';
	import ErrorMessage from './ErrorMessage.svelte';
	import { supabase } from '$lib/db/supabaseClient';
	import { wallet } from '$lib/stores/wallet';

	// ===================
	// PROPS & STATIC DATA
	// ===================
	export let data = {};

	const prebuiltVoices = [
		{
			id: 's3://voice-cloning-zero-shot/e46b4027-b38d-4d24-b292-38fbca2be0ef/original/manifest.json',
			name: 'Apex',
			voiceIndex: 0
		},
		{
			id: 's3://voice-cloning-zero-shot/743575eb-efdc-4c10-b185-a5018148822f/original/manifest.json',
			name: 'Felix',
			voiceIndex: 1
		},
		{
			id: 's3://voice-cloning-zero-shot/7c339a9d-370f-4643-adf5-4134e3ec9886/mlae02/manifest.json',
			name: 'Isaac',
			voiceIndex: 2
		},
		{
			id: 's3://voice-cloning-zero-shot/80ba8839-a6e6-470c-8f68-7c1e5d3ee2ff/abigailsaad/manifest.json',
			name: 'Avarice',
			voiceIndex: 3
		},
		{
			id: 's3://voice-cloning-zero-shot/f6c4ed76-1b55-4cd9-8896-31f7535f6cdb/original/manifest.json',
			name: 'Archive',
			voiceIndex: 4
		},
		{
			id: 's3://voice-cloning-zero-shot/90217770-a480-4a91-b1ea-df00f4d4c29d/original/manifest.json',
			name: 'Rose',
			voiceIndex: 5
		},
		{
			id: 's3://voice-cloning-zero-shot/a540a448-a9ca-446c-9538-d1bae6c506f1/original/manifest.json',
			name: 'Prometheus',
			voiceIndex: 6
		},
		{
			id: 's3://voice-cloning-zero-shot/dc90b58b-59a9-4e65-955d-c7620deb2d7a/original/manifest.json',
			name: 'Caesium',
			voiceIndex: 7
		},
		{
			id: 's3://voice-cloning-zero-shot/f43cc4b4-b193-4a13-a903-e6b125c3d572/original/manifest.json',
			name: 'Sumatra',
			voiceIndex: 8
		}
	];

	// ===================
	// STATE VARIABLES
	// ===================

	// Input state
	let text = '';
	let selectedVoiceType = null; // null, 'prebuilt', or 'clone'
	let selectedPrebuiltVoice = null;
	let customVoiceFile = null;
	let customVoiceUrl = null;

	// Generation state
	let isLoading = false;
	let error = null;

	// Result state
	let audioUrl = '';
	let resultSpeaker = '';

	// Voice clone state
	let myClone = null;
	let isLoadingClone = false;

	// Audio preview state
	let currentPlayingAudio = null;
	let currentPlayingVoice = null;
	let speechSynthesis = null;
	let availableVoices = [];
	let sampleAudioInstances = new Map();

	// Modal state
	let isOpenHelp = false;

	// Audio player state (from VoiceResult)
	let wavesurferComponent;
	let duration = 0;
	let currentTime = 0;
	let isPlaying = false;
	let isMuted = false;
	let isReady = false;

	// ========================================
	// CATEGORY 1: FETCHING FROM DATABASE
	// ========================================

	async function checkOwnClone() {
		if (!address) return;

		isLoadingClone = true;
		try {
			const response = await fetch(
				`/api/playground/tts/get-voice-clone?address=${encodeURIComponent(address)}`
			);

			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}

			const data = await response.json();
			myClone = data.voice_clone_id || null;
			console.log('Own clone data:', myClone);
		} catch (error) {
			console.error('Error checking own clone:', error);
			myClone = null;
		} finally {
			isLoadingClone = false;
		}
	}

	// ========================================
	// CATEGORY 2: REACTIVITY ONLY
	// ========================================

	// Reactive address from props or wallet
	$: address = data?.address || $wallet?.address || '';

	// Computed values
	$: canGenerate = text.trim().length > 0 && selectedVoiceType && !isLoading;
	$: hasResult = audioUrl && !isLoading;

	// Reset state when audioUrl changes
	$: if (audioUrl) {
		cleanupAudioPlayer();
	}

	// ===================
	// UI INTERACTION HANDLERS
	// ===================

	function handleTextInput(event) {
		text = event.target.value;
	}

	function handleKeydown(event) {
		if (
			event.key === 'Enter' &&
			!event.shiftKey &&
			!event.ctrlKey &&
			!event.altKey &&
			!event.metaKey
		) {
			event.preventDefault();
			if (canGenerate) {
				generateSpeech();
			}
		}
	}

	function selectPrebuiltVoice(voiceId) {
		selectedVoiceType = 'prebuilt';
		selectedPrebuiltVoice = voiceId;
		// Don't clear customVoiceFile - let user keep it for potential cloning
		// customVoiceFile = null;
		// customVoiceUrl = null;
		// This will automatically deactivate clone since selectedVoiceType changes
	}

	function handleVoiceUpload(event) {
		const file = event.target.files?.[0];
		if (file && file.type.startsWith('audio/')) {
			customVoiceFile = file;
			customVoiceUrl = URL.createObjectURL(file);
			selectedPrebuiltVoice = null;
			// Reset selectedVoiceType to allow cloning of custom voice
			selectedVoiceType = null;
		}
	}

	function triggerVoiceUpload() {
		document.getElementById('voice-upload').click();
	}

	function toggleModal() {
		isOpenHelp = !isOpenHelp;
	}

	function removeCustomVoice() {
		customVoiceFile = null;
		customVoiceUrl = null;
		selectedVoiceType = null;
		selectedPrebuiltVoice = null;
		// Reset the file input
		const fileInput = document.getElementById('voice-upload');
		if (fileInput) fileInput.value = '';
	}

	async function handleUploadClone() {
		if (!customVoiceFile) {
			triggerVoiceUpload();
			return;
		}

		if (!address) {
			error = 'Please connect your wallet first';
			return;
		}

		isLoadingClone = true;
		error = null;

		try {
			const formData = new FormData();
			formData.append('file', customVoiceFile);
			formData.append('address', address);

			const response = await fetch('/api/playground/tts/voice-clone', {
				method: 'POST',
				body: formData
			});

			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}

			const data = await response.json();
			myClone = data.id;
			customVoiceFile = null;
			customVoiceUrl = null;
			// Reset voice selection to use the new clone
			selectedVoiceType = 'clone';
			selectedPrebuiltVoice = null;
			// Reset the file input
			const fileInput = document.getElementById('voice-upload');
			if (fileInput) fileInput.value = '';

			console.log('Voice clone created:', data);
		} catch (err) {
			error = err.message || 'Failed to create voice clone';
			console.error('Error creating voice clone:', err);
		} finally {
			isLoadingClone = false;
		}
	}

	async function handleDeleteClone() {
		if (!address || !myClone) return;

		isLoadingClone = true;
		error = null;

		try {
			const response = await fetch('/api/playground/tts/delete-voice-clone', {
				method: 'DELETE',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ address })
			});

			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}

			const data = await response.json();
			myClone = null;
			selectedVoiceType = null;

			console.log('Voice clone deleted:', data);
		} catch (err) {
			error = err.message || 'Failed to delete voice clone';
			console.error('Error deleting voice clone:', err);
		} finally {
			isLoadingClone = false;
		}
	}

	function handleToggleClone() {
		if (!myClone) return;

		if (selectedVoiceType === 'clone') {
			// If clone is currently active, deactivate it
			selectedVoiceType = null;
		} else {
			// If clone is not active, activate it and deselect prebuilt voices
			selectedVoiceType = 'clone';
			selectedPrebuiltVoice = null;
		}
	}

	// Error handling
	function clearError() {
		error = null;
	}

	// ===================
	// AUDIO PLAYER CONTROLS
	// ===================

	function togglePlayPause() {
		const wavesurfer = wavesurferComponent?.getWaveSurfer();
		if (!wavesurfer || !isReady) return;

		if (wavesurfer.isPlaying()) {
			wavesurfer.pause();
		} else {
			wavesurfer.play();
		}
	}

	function skipBackward() {
		const wavesurfer = wavesurferComponent?.getWaveSurfer();
		if (!wavesurfer || !duration || !isReady) return;
		const newTime = Math.max(0, currentTime - 10);
		const seekPosition = newTime / duration;
		wavesurfer.seekTo(seekPosition);
		currentTime = newTime;
	}

	function skipForward() {
		const wavesurfer = wavesurferComponent?.getWaveSurfer();
		if (!wavesurfer || !duration || !isReady) return;
		const newTime = Math.min(duration, currentTime + 10);
		const seekPosition = newTime / duration;
		wavesurfer.seekTo(seekPosition);
		currentTime = newTime;
	}

	// ===================
	// WAVESURFER EVENT HANDLERS
	// ===================

	function handleReady() {
		const wavesurfer = wavesurferComponent?.getWaveSurfer();
		if (wavesurfer) {
			duration = wavesurfer.getDuration();
			isReady = true;
			console.log('WaveSurfer ready, duration:', duration);
		}
	}

	function handleAudioProcess() {
		const wavesurfer = wavesurferComponent?.getWaveSurfer();
		if (wavesurfer && isReady) {
			currentTime = wavesurfer.getCurrentTime();
		}
	}

	function handleSeek() {
		const wavesurfer = wavesurferComponent?.getWaveSurfer();
		if (wavesurfer && isReady) {
			currentTime = wavesurfer.getCurrentTime();
		}
	}

	function handlePlay() {
		isPlaying = true;
	}

	function handlePause() {
		isPlaying = false;
	}

	function handleFinish() {
		isPlaying = false;
		// Reset to beginning after a short delay
		setTimeout(() => {
			const wavesurfer = wavesurferComponent?.getWaveSurfer();
			if (wavesurfer && isReady) {
				wavesurfer.seekTo(0);
				currentTime = 0;
			}
		}, 1000);
	}

	function handleError(error) {
		console.error('WaveSurfer error:', error);
		isReady = false;
	}

	function cleanupAudioPlayer() {
		isPlaying = false;
		currentTime = 0;
		duration = 0;
		isMuted = false;
		isReady = false;
	}

	// ===================
	// UTILITY FUNCTIONS
	// ===================

	function formatTime(seconds) {
		if (!seconds || !isFinite(seconds)) return '0:00';
		const mins = Math.floor(seconds / 60);
		const secs = Math.floor(seconds % 60);
		return `${mins}:${secs.toString().padStart(2, '0')}`;
	}

	function handleDownloadVoice() {
		if (audioUrl) {
			const link = document.createElement('a');
			link.href = audioUrl;
			link.download = `generated-speech-${resultSpeaker.toLowerCase().replace(/\s+/g, '-')}.wav`;
			document.body.appendChild(link);
			link.click();
			document.body.removeChild(link);
		}
	}

	// ===================
	// SAMPLE VOICE PLAYBACK
	// ===================

	async function handlePlaySample(voiceId) {
		// Stop any currently playing voice
		if (currentPlayingVoice) {
			const currentAudio = sampleAudioInstances.get(currentPlayingVoice);
			if (currentAudio) {
				currentAudio.pause();
				currentAudio.currentTime = 0;
			}
			currentPlayingVoice = null;
		}

		// Find the voice to get its index for the sample file
		const voice = prebuiltVoices.find((v) => v.id === voiceId);
		if (!voice) return;

		// Create sample file path based on voice index
		const samplePath = `/samples/voice-${voice.voiceIndex}.wav`;

		try {
			// Get or create audio instance
			let audio = sampleAudioInstances.get(voiceId);
			if (!audio) {
				audio = new Audio(samplePath);
				audio.preload = 'auto';
				sampleAudioInstances.set(voiceId, audio);

				// Set up event listeners
				audio.addEventListener('ended', () => {
					currentPlayingVoice = null;
				});

				audio.addEventListener('error', (e) => {
					console.error('Error playing sample:', e);
					currentPlayingVoice = null;
				});
			}

			// Set current playing voice and play
			currentPlayingVoice = voiceId;
			audio.currentTime = 0;
			await audio.play();
		} catch (error) {
			console.error('Error playing sample:', error);
			currentPlayingVoice = null;
		}
	}

	// ===================
	// SPEECH GENERATION
	// ===================

	async function generateSpeech() {
		// Validation
		if (!text.trim()) {
			error = 'Please enter some text to convert to speech';
			return;
		}

		if (text.trim().length < 3) {
			error = 'Text must be at least 3 characters long';
			return;
		}

		if (!selectedVoiceType) {
			error = 'Please select a voice before generating speech';
			return;
		}

		if (isLoading) {
			error = 'Please wait for the current operation to finish';
			return;
		}

		// Reset state
		isLoading = true;
		error = null;
		audioUrl = '';

		console.log('Generating speech with:', {
			text: text.trim(),
			selectedVoiceType,
			selectedPrebuiltVoice,
			customVoiceFile
		});

		try {
			console.log('Starting speech generation...');

			// Prepare request data
			const requestData = {
				text: text.trim()
			};

			// Add voice parameter based on selection
			if (selectedVoiceType === 'prebuilt') {
				console.log('Using prebuilt voice:', selectedPrebuiltVoice);
				requestData.voice = selectedPrebuiltVoice;
			} else if (selectedVoiceType === 'clone') {
				console.log('Using custom voice clone:', myClone);
				requestData.voice = myClone;
			} else {
				console.error('Invalid voice type selected:', selectedVoiceType);
				error = 'Please select a valid voice type';
				return;
			}

			// Call TTS API
			const response = await fetch('/api/playground/tts/tts', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(requestData)
			});

			if (!response.ok) {
				const errorData = await response.json();
				throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
			}

			// Create audio blob and URL
			const audioBlob = await response.blob();
			const generatedAudioUrl = URL.createObjectURL(audioBlob);

			// Update result state
			audioUrl = generatedAudioUrl;
			resultSpeaker =
				selectedVoiceType === 'prebuilt'
					? prebuiltVoices.find((v) => v.id === selectedPrebuiltVoice)?.name || 'Unknown Voice'
					: selectedVoiceType === 'clone'
						? 'My Clone'
						: 'Generated Voice';

			console.log('Speech generation completed successfully');
		} catch (err) {
			error = err.message || 'An error occurred while generating the speech';
			console.error('Error generating speech:', err);
		} finally {
			isLoading = false;
		}
	}

	// ===================
	// LIFECYCLE HOOKS
	// ===================

	onMount(async () => {
		await checkOwnClone();

		// Initialize speech synthesis
		if ('speechSynthesis' in window) {
			speechSynthesis = window.speechSynthesis;

			// Load voices
			const loadVoices = () => {
				availableVoices = speechSynthesis.getVoices();
			};

			// Load voices immediately and on voiceschanged event
			loadVoices();
			speechSynthesis.onvoiceschanged = loadVoices;
		}
	});

	onDestroy(() => {
		cleanupAudioPlayer();

		// Cleanup sample audio instances
		sampleAudioInstances.forEach((audio) => {
			audio.pause();
			audio.src = '';
		});
		sampleAudioInstances.clear();
	});
</script>

<svelte:head>
	<title>Text to Speech</title>
	<meta
		name="description"
		content="Explore Tensorone's AI-powered Text to Speech tool. Convert your text into natural-sounding speech in our interactive playground section."
	/>
</svelte:head>

<Header />

<section class="min-h-screen w-full shadow-sm relative p-8 flex flex-col">
	<PageTitle subtitle="Playground" title="Text to Speech" {address} />

	<!-- Error Message Component -->
	{#if error}
		<ErrorMessage {error} onClear={clearError} />
	{/if}

	<div class="flex flex-1 gap-8 min-h-0">
		<!-- Controls Panel -->
		<div class="xl:w-2/5">
			<div class="flex-1 overflow-y-auto pr-2">
				<!-- Text Input -->
				<TextInput bind:text {isLoading} onInput={handleTextInput} onKeydown={handleKeydown} />

				<!-- Voice Clone Section -->
				<VoiceClone
					{customVoiceFile}
					{myClone}
					{isLoadingClone}
					{address}
					{selectedVoiceType}
					onVoiceUpload={handleVoiceUpload}
					onTriggerUpload={triggerVoiceUpload}
					onRemoveVoice={removeCustomVoice}
					onToggleModal={toggleModal}
					onUploadClone={handleUploadClone}
					onDeleteClone={handleDeleteClone}
					onToggleClone={handleToggleClone}
				/>

				<!-- Prebuilt Models Section -->
				<PrebuiltVoices
					{prebuiltVoices}
					{selectedVoiceType}
					{selectedPrebuiltVoice}
					{currentPlayingVoice}
					onSelectVoice={selectPrebuiltVoice}
					onPlaySample={handlePlaySample}
				/>
			</div>

			<!-- Generate Button -->
			<GenerateButton {canGenerate} {isLoading} onGenerate={generateSpeech} />
		</div>

		<!-- Result Section -->
		<div
			class="xl:w-3/5 min-h-0"
			in:fade|global={{ delay: 550, duration: 500 }}
			out:fade|global={{ duration: 300 }}
		>
			<VoiceResult
				{audioUrl}
				{isLoading}
				onDownloadVoice={handleDownloadVoice}
				bind:wavesurferComponent
				{duration}
				{currentTime}
				{isPlaying}
				{isReady}
				{formatTime}
				onTogglePlayPause={togglePlayPause}
				onSkipBackward={skipBackward}
				onSkipForward={skipForward}
				onReady={handleReady}
				onPlay={handlePlay}
				onPause={handlePause}
				onAudioProcess={handleAudioProcess}
				onSeek={handleSeek}
				onFinish={handleFinish}
				onError={handleError}
			/>
		</div>
	</div>

	<!-- Help Modal -->
	<HelpModal {isOpenHelp} onToggleModal={toggleModal} />
</section>
