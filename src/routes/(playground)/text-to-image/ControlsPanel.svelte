<script>
	import PromptInput from './PromptInput.svelte';
	import AspectRatioSelector from './AspectRatioSelector.svelte';
	import StyleSelector from './StyleSelector.svelte';
	import GenerateButton from './GenerateButton.svelte';

	export let prompt;
	export let selectedModel;
	export let activeRatio;
	export let modelOptions;
	export let aspectRatios;
	export let isLoading;
	export let canGenerate;
	export let onPromptInput;
	export let onModelChange;
	export let onRatioSelect;
	export let onKeydown;
	export let onGenerate;
</script>

<div class="xl:w-2/5">
	<div class="flex-1 overflow-y-auto pr-2">
		<PromptInput bind:prompt {isLoading} onInput={onPromptInput} {onKeydown} />

		<AspectRatioSelector {aspectRatios} {activeRatio} {isLoading} {onRatioSelect} />

		<StyleSelector {modelOptions} {selectedModel} {isLoading} {onModelChange} />
	</div>

	<GenerateButton {canGenerate} {isLoading} {onGenerate} />
</div>
