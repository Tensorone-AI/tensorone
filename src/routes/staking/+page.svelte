<script>
	import Header from '../Header.svelte';
	import ComingSoon from '../ComingSoon.svelte';
</script>

<svelte:head>
	<title>Staking</title>
	<meta
		name="description"
		content="Stay tuned for Tensorone's upcoming staking feature. Soon you'll be able to stake $TPO tokens and earn rewards. More details coming soon!"
	/>
</svelte:head>

<Header />

<section class="w-full h-screen relative overflow-hidden">
	<ComingSoon
		description="Stake $TPO and earn a share of revenue generated from the Tensor ecosystem, proportional to your holdings."
	/>
</section>
