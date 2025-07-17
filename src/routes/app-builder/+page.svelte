<script>
	import Header from '../Header.svelte';
	import ComingSoon from '../ComingSoon.svelte';
</script>

<svelte:head>
	<title>App Builder</title>
	<meta
		name="description"
		content="Stay tuned for Tensorone's upcoming staking feature. Soon you'll be able to stake $TPO tokens and earn rewards. More details coming soon!"
	/>
</svelte:head>

<Header />

<section class="w-full h-screen flex relative overflow-hidden bg-[#060606BF]">
	<ComingSoon
		description="Effortlessly design and launch custom applications with AI-powered tools. Use intelligent features and templates to turn your ideas into reality."
	/>
</section>
